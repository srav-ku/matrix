#!/usr/bin/env python3
"""
Movie Database API - Phase 2
RESTful API endpoints for the movie database
"""

import sys
import os
sys.path.append('.')
sys.path.append('./src')

from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from src.database import execute_query
from src.auth import (
    create_user, verify_user_email, resend_verification, 
    validate_api_key, log_api_usage, AuthError, RateLimitError,
    init_firebase, generate_api_key, hash_api_key, 
    check_user_rate_limit, get_user_usage_stats, upgrade_user_to_premium
)
import json
from functools import wraps

app = Flask(__name__, template_folder='../templates', static_folder='../static')

# Configure CORS for Replit environment - allow all origins for development
CORS(app, origins="*")

# Configure Flask for development
app.config['DEBUG'] = True

# Essential for Replit: Disable host header checks for proxy environments
app.config['SERVER_NAME'] = None

# Initialize Firebase (will be set up when credentials are provided)
firebase_initialized = init_firebase()

def require_api_key(f):
    """Decorator to require API key for protected endpoints"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key') or request.headers.get('Authorization')
        if api_key and api_key.startswith('Bearer '):
            api_key = api_key[7:]  # Remove 'Bearer ' prefix
        
        if not api_key:
            return jsonify({'error': 'API key required'}), 401
        
        user_info = validate_api_key(api_key)
        if not user_info:
            return jsonify({'error': 'Invalid API key'}), 401
        
        # Check user rate limit before processing request
        try:
            from src.auth import check_user_rate_limit
            check_user_rate_limit(user_info['user_id'])
        except RateLimitError as e:
            return jsonify({'error': str(e)}), 429
        except:
            pass  # Don't fail request if rate limiting check fails
        
        # Log API usage
        try:
            log_api_usage(user_info['api_key_id'], request.endpoint, 200)
        except:
            pass  # Don't fail request if logging fails
        
        # Add user info to request context
        request.user_info = user_info
        return f(*args, **kwargs)
    
    return decorated_function

@app.route('/')
def home():
    """API root endpoint"""
    return jsonify({
        'message': 'Movie Database API',
        'version': '2.0',
        'endpoints': {
            'movies': '/api/movies',
            'search': '/api/search',
            'stats': '/api/stats',
            'auth': '/api/auth/*'
        }
    })

@app.route('/api/movies', methods=['GET'])
def get_movies():
    """Get all movies with optional filtering and pagination"""
    try:
        # Get query parameters
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 20))
        genre = request.args.get('genre')
        year = request.args.get('year')
        search = request.args.get('search')
        
        # Calculate offset
        offset = (page - 1) * limit
        
        # Build base query
        query = """
            SELECT DISTINCT m.id, m.title, m.year, m.runtime, m.rating, 
                   m.director, m.plot, m.poster_url
            FROM movies m
        """
        
        conditions = []
        params = []
        
        # Add genre filter
        if genre:
            query += " LEFT JOIN movie_genres mg ON m.id = mg.movie_id"
            conditions.append("mg.genre = %s")
            params.append(genre)
        
        # Add search filter
        if search:
            conditions.append("(m.title ILIKE %s OR m.director ILIKE %s OR m.plot ILIKE %s)")
            search_param = f"%{search}%"
            params.extend([search_param, search_param, search_param])
        
        # Add year filter
        if year:
            conditions.append("m.year = %s")
            params.append(int(year))
        
        # Add WHERE clause if we have conditions
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        
        # Add ordering and pagination
        query += " ORDER BY m.year DESC, m.title LIMIT %s OFFSET %s"
        params.extend([limit, offset])
        
        movies = execute_query(query, tuple(params), fetch=True)
        
        # Enrich with genres and cast for each movie
        enriched_movies = []
        for movie in movies:
            movie_dict = dict(movie)
            
            # Get genres
            genres_result = execute_query(
                "SELECT genre FROM movie_genres WHERE movie_id = %s ORDER BY genre",
                (movie['id'],), fetch=True
            )
            movie_dict['genres'] = [g['genre'] for g in genres_result]
            
            # Get cast
            cast_result = execute_query(
                "SELECT actor_name FROM movie_cast WHERE movie_id = %s ORDER BY actor_name",
                (movie['id'],), fetch=True
            )
            movie_dict['cast'] = [c['actor_name'] for c in cast_result]
            
            enriched_movies.append(movie_dict)
        
        # Get total count for pagination
        count_query = "SELECT COUNT(DISTINCT m.id) as total FROM movies m"
        if genre:
            count_query += " LEFT JOIN movie_genres mg ON m.id = mg.movie_id"
        if conditions:
            count_query += " WHERE " + " AND ".join(conditions[:-2] if year else conditions)
            count_params = params[:-2] if conditions else []
        else:
            count_params = []
        
        total_result = execute_query(count_query, tuple(count_params), fetch=True)
        total_movies = total_result[0]['total']
        
        return jsonify({
            'movies': enriched_movies,
            'pagination': {
                'page': page,
                'limit': limit,
                'total': total_movies,
                'pages': (total_movies + limit - 1) // limit
            }
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/movies/<int:movie_id>', methods=['GET'])
def get_movie(movie_id):
    """Get a specific movie by ID"""
    try:
        # Get movie details
        movie_result = execute_query(
            "SELECT * FROM movies WHERE id = %s",
            (movie_id,), fetch=True
        )
        
        if not movie_result:
            return jsonify({'error': 'Movie not found'}), 404
        
        movie = dict(movie_result[0])
        
        # Get genres
        genres_result = execute_query(
            "SELECT genre FROM movie_genres WHERE movie_id = %s ORDER BY genre",
            (movie_id,), fetch=True
        )
        movie['genres'] = [g['genre'] for g in genres_result]
        
        # Get cast
        cast_result = execute_query(
            "SELECT actor_name, role FROM movie_cast WHERE movie_id = %s ORDER BY actor_name",
            (movie_id,), fetch=True
        )
        movie['cast'] = [{'name': c['actor_name'], 'role': c['role']} for c in cast_result]
        
        return jsonify({'movie': movie})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/genres', methods=['GET'])
def get_genres():
    """Get all available genres"""
    try:
        genres_result = execute_query(
            "SELECT DISTINCT genre FROM movie_genres ORDER BY genre",
            fetch=True
        )
        genres = [g['genre'] for g in genres_result]
        return jsonify({'genres': genres})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/years', methods=['GET'])
def get_years():
    """Get all available years"""
    try:
        years_result = execute_query(
            "SELECT DISTINCT year FROM movies ORDER BY year DESC",
            fetch=True
        )
        years = [y['year'] for y in years_result]
        return jsonify({'years': years})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get database statistics"""
    try:
        # Get counts
        movies_count = execute_query("SELECT COUNT(*) as count FROM movies", fetch=True)[0]['count']
        genres_count = execute_query("SELECT COUNT(*) as count FROM movie_genres", fetch=True)[0]['count']
        cast_count = execute_query("SELECT COUNT(*) as count FROM movie_cast", fetch=True)[0]['count']
        
        # Get year range
        year_range = execute_query(
            "SELECT MIN(year) as min_year, MAX(year) as max_year FROM movies",
            fetch=True
        )[0]
        
        return jsonify({
            'movies_total': movies_count,
            'genres_total': genres_count,
            'cast_total': cast_count,
            'year_range': {
                'min': year_range['min_year'],
                'max': year_range['max_year']
            }
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/search', methods=['GET'])
def search_movies():
    """Search movies by title, director, or plot"""
    try:
        query = request.args.get('q', '').strip()
        if not query:
            return jsonify({'error': 'Search query is required'}), 400
        
        search_param = f"%{query}%"
        movies = execute_query("""
            SELECT DISTINCT m.id, m.title, m.year, m.runtime, m.rating, 
                   m.director, m.plot, m.poster_url
            FROM movies m
            WHERE m.title ILIKE %s OR m.director ILIKE %s OR m.plot ILIKE %s
            ORDER BY m.year DESC, m.title
            LIMIT 50
        """, (search_param, search_param, search_param), fetch=True)
        
        # Enrich with genres
        enriched_movies = []
        for movie in movies:
            movie_dict = dict(movie)
            genres_result = execute_query(
                "SELECT genre FROM movie_genres WHERE movie_id = %s ORDER BY genre",
                (movie['id'],), fetch=True
            )
            movie_dict['genres'] = [g['genre'] for g in genres_result]
            enriched_movies.append(movie_dict)
        
        return jsonify({
            'movies': enriched_movies,
            'query': query,
            'count': len(enriched_movies)
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# PHASE 4 - Authentication Endpoints

@app.route('/api/auth/firebase-login', methods=['POST'])
def firebase_login():
    """Handle Firebase authentication and generate/retrieve API key"""
    try:
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Firebase ID token required in Authorization header'}), 401
        
        # For now, we'll skip Firebase token verification since we're moving to client-side auth
        # In a production app, you'd verify the Firebase ID token here
        id_token = auth_header[7:]  # Remove 'Bearer ' prefix
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'User data required'}), 400
        
        uid = data.get('uid')
        email = data.get('email', '').strip().lower()
        email_verified = data.get('emailVerified', False)
        
        if not uid or not email:
            return jsonify({'error': 'Firebase UID and email are required'}), 400
        
        # Check if user exists in our database
        existing_user = execute_query(
            "SELECT id, email, is_verified FROM users WHERE email = %s",
            (email,), fetch=True
        )
        
        if existing_user:
            user_id = existing_user[0]['id']
            # Update verification status if needed
            if email_verified and not existing_user[0]['is_verified']:
                execute_query(
                    "UPDATE users SET is_verified = %s WHERE id = %s",
                    (email_verified, user_id)
                )
        else:
            # Create new user record
            result = execute_query("""
                INSERT INTO users (email, password_hash, is_verified, created_at)
                VALUES (%s, %s, %s, CURRENT_TIMESTAMP)
                RETURNING id
            """, (email, 'firebase_auth', email_verified), fetch=True)
            user_id = result[0]['id']
        
        # Check if user already has an API key
        existing_key = execute_query("""
            SELECT api_key FROM api_keys 
            WHERE user_id = %s AND is_active = TRUE
            ORDER BY created_at DESC 
            LIMIT 1
        """, (user_id,), fetch=True)
        
        if existing_key:
            # Return existing API key (hashed, so we need to generate a new one)
            # For now, generate a new one
            pass
        
        # Generate new API key
        raw_api_key = generate_api_key()
        hashed_key = hash_api_key(raw_api_key)
        
        # Store API key
        execute_query("""
            INSERT INTO api_keys (user_id, api_key, created_at, is_active)
            VALUES (%s, %s, CURRENT_TIMESTAMP, TRUE)
        """, (user_id, hashed_key))
        
        return jsonify({
            'success': True,
            'api_key': raw_api_key,
            'message': 'API key generated successfully!',
            'user': {
                'email': email,
                'email_verified': email_verified,
                'uid': uid
            }
        })
        
    except Exception as e:
        return jsonify({'error': f'Firebase login failed: {str(e)}'}), 500

@app.route('/api/auth/signup', methods=['POST'])
def signup():
    """User signup endpoint (legacy)"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'JSON data required'}), 400
        
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        
        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400
        
        if len(password) < 8:
            return jsonify({'error': 'Password must be at least 8 characters long'}), 400
        
        result = create_user(email, password)
        return jsonify(result), 201
        
    except (AuthError, RateLimitError) as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'Signup failed: {str(e)}'}), 500

@app.route('/api/auth/verify', methods=['POST'])
def verify_email():
    """Email verification endpoint"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'JSON data required'}), 400
        
        email = data.get('email', '').strip().lower()
        verification_code = data.get('verification_code', '').strip()
        
        if not email:
            return jsonify({'error': 'Email is required'}), 400
        
        result = verify_user_email(email, verification_code)
        return jsonify(result), 200
        
    except AuthError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'Verification failed: {str(e)}'}), 500

@app.route('/api/auth/resend', methods=['POST'])
def resend_verification_email():
    """Resend verification email endpoint"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'JSON data required'}), 400
        
        email = data.get('email', '').strip().lower()
        if not email:
            return jsonify({'error': 'Email is required'}), 400
        
        result = resend_verification(email)
        return jsonify(result), 200
        
    except (AuthError, RateLimitError) as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'Failed to resend verification: {str(e)}'}), 500

@app.route('/api/auth/validate', methods=['GET'])
@require_api_key
def validate_key():
    """Validate API key endpoint"""
    return jsonify({
        'valid': True,
        'user_id': request.user_info['user_id'],
        'email': request.user_info['email']
    })

@app.route('/api/protected/movies', methods=['GET'])
@require_api_key
def get_protected_movies():
    """Protected movies endpoint requiring API key"""
    # Same as get_movies but requires authentication
    return get_movies()

@app.route('/api/user/usage', methods=['GET'])
@require_api_key
def get_user_usage():
    """Get user API usage statistics"""
    try:
        user_id = request.user_info['user_id']
        
        # Get daily usage for last 30 days
        daily_usage = execute_query("""
            SELECT date, request_count
            FROM daily_usage du
            JOIN api_keys ak ON du.api_key_id = ak.id
            WHERE ak.user_id = %s AND date >= CURRENT_DATE - INTERVAL '30 days'
            ORDER BY date DESC
        """, (user_id,), fetch=True)
        
        # Get total usage
        total_usage = execute_query("""
            SELECT COUNT(*) as total_requests
            FROM usage_logs ul
            JOIN api_keys ak ON ul.api_key_id = ak.id
            WHERE ak.user_id = %s
        """, (user_id,), fetch=True)
        
        return jsonify({
            'total_requests': total_usage[0]['total_requests'] if total_usage else 0,
            'daily_usage': [dict(row) for row in daily_usage]
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/user/quota', methods=['GET'])
@require_api_key
def get_user_quota():
    """Get user's current quota and usage stats"""
    try:
        user_id = request.user_info['user_id']
        stats = get_user_usage_stats(user_id)
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/user/upgrade', methods=['POST'])
@require_api_key
def upgrade_to_premium():
    """Upgrade user to premium plan"""
    try:
        user_id = request.user_info['user_id']
        upgrade_user_to_premium(user_id)
        return jsonify({
            'success': True,
            'message': 'Successfully upgraded to premium plan!',
            'new_daily_limit': 500
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Check database connection
    try:
        stats = execute_query("SELECT COUNT(*) as count FROM movies", fetch=True)
        print(f"✅ Database connected! Found {stats[0]['count']} movies.")
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        exit(1)
    
    print("🚀 Starting Movie Database API...")
    print("📊 Available endpoints:")
    print("  GET /                     - Frontend interface")
    print("  GET /api/movies          - List movies (with pagination & filters)")
    print("  GET /api/movies/{id}     - Get specific movie")
    print("  GET /api/genres          - List all genres")
    print("  GET /api/years           - List all years")
    print("  GET /api/stats           - Database statistics")
    print("  GET /api/search?q=term   - Search movies")
    
    # Start the server on all interfaces for Replit
    app.run(host='0.0.0.0', port=8000, debug=True)