#!/usr/bin/env python3
"""
Enhanced Movie Database API with Authentication and Usage Tracking
"""

import sys
import os
from functools import wraps
sys.path.append('.')
sys.path.append('./src')

from flask import Flask, jsonify, request
from flask_cors import CORS
from src.database import execute_query
from src.auth_api import AuthManager
from src.auth import (
    check_user_rate_limit, check_and_increment_user_rate_limit, get_user_usage_stats, 
    upgrade_user_to_premium, RateLimitError, validate_firebase_admin, init_firebase
)

app = Flask(__name__)

# Configure CORS for Replit environment
CORS(app, origins="*")

# Configure Flask for development
app.config['DEBUG'] = True
app.config['SERVER_NAME'] = None

def require_firebase_admin(f):
    """Decorator to require Firebase admin authentication for admin endpoints"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Initialize Firebase if not already done
        init_firebase()
        
        # Get Firebase token from Authorization header
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({
                'error': 'Firebase admin authentication required', 
                'message': 'Include Firebase ID token in Authorization header as Bearer token'
            }), 401
        
        firebase_token = auth_header.split('Bearer ')[1]
        
        # Validate Firebase admin token for specific admin UID
        admin_uid = "MF2LvHPFaWhWSoevxm4ZyLcZzme2"
        if not validate_firebase_admin(firebase_token, admin_uid):
            return jsonify({
                'error': 'Admin access denied', 
                'message': 'Only specific admin user can access these endpoints'
            }), 403
        
        # Add admin info to request
        request.admin_info = {
            'firebase_uid': admin_uid,
            'role': 'admin',
            'email': 'admin@moviedb.com'
        }
        
        return f(*args, **kwargs)
    return decorated_function

# Admin endpoints (protected by Firebase authentication)
@app.route('/admin/movies', methods=['GET'])
@require_firebase_admin
def admin_list_movies():
    """Admin endpoint to list all movies with pagination"""
    try:
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 20, type=int)
        offset = (page - 1) * limit
        
        # Get total count
        count_result = execute_query("SELECT COUNT(*) as total FROM movies", fetch=True)
        total = count_result[0]['total'] if count_result else 0
        
        # Get movies with pagination
        movies = execute_query("""
            SELECT m.*, 
                   STRING_AGG(DISTINCT mg.genre, ', ') as genres,
                   STRING_AGG(DISTINCT CONCAT(c.actor_name, ' as ', c.role), '; ') as cast
            FROM movies m
            LEFT JOIN movie_genres mg ON m.id = mg.movie_id  
            LEFT JOIN movie_cast c ON m.id = c.movie_id
            GROUP BY m.id
            ORDER BY m.year DESC, m.title
            LIMIT %s OFFSET %s
        """, (limit, offset), fetch=True)
        
        pages = (total + limit - 1) // limit
        
        return jsonify({
            'movies': movies or [],
            'pagination': {
                'page': page,
                'limit': limit,
                'total': total,
                'pages': pages
            },
            'admin': True
        })
    except Exception as e:
        return jsonify({'error': f'Admin movies list failed: {str(e)}'}), 500

@app.route('/admin/movies/upload-csv', methods=['POST'])
@require_firebase_admin
def admin_upload_csv():
    """Admin endpoint to upload CSV file and update database"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No CSV file provided'}), 400
        
        file = request.files['file']
        if not file or file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not file.filename.lower().endswith('.csv'):
            return jsonify({'error': 'File must be CSV format'}), 400
        
        # Read CSV content
        import csv
        import io
        
        stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
        csv_input = csv.DictReader(stream)
        
        movies_added = 0
        movies_updated = 0
        errors = []
        
        for row_num, row in enumerate(csv_input, start=2):
            try:
                # Validate required fields
                required_fields = ['title', 'year', 'genre', 'runtime']
                missing_fields = [field for field in required_fields if not row.get(field)]
                
                if missing_fields:
                    errors.append(f"Row {row_num}: Missing fields: {', '.join(missing_fields)}")
                    continue
                
                # Insert or update movie
                movie_result = execute_query("""
                    INSERT INTO movies (title, year, runtime, rating, poster_url, director, plot, external_id)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (title, year) DO UPDATE SET
                        runtime = EXCLUDED.runtime,
                        rating = EXCLUDED.rating,
                        poster_url = EXCLUDED.poster_url,
                        director = EXCLUDED.director,
                        plot = EXCLUDED.plot,
                        external_id = EXCLUDED.external_id
                    RETURNING id, title, (xmax = 0) as inserted
                """, (
                    row.get('title', '').strip(),
                    int(row.get('year', 0)),
                    int(row.get('runtime', 0)),
                    float(row.get('rating', 0)) if row.get('rating') else None,
                    row.get('poster_url', '').strip(),
                    row.get('director', '').strip(),
                    row.get('plot', '').strip(),
                    row.get('external_id', '').strip() or None
                ), fetch=True)
                
                if movie_result:
                    movie_id = movie_result[0]['id']
                    
                    # Process and insert genres
                    genres_text = row.get('genre', '').strip()
                    if genres_text:
                        # Clear existing genres for this movie (in case of update)
                        execute_query("DELETE FROM movie_genres WHERE movie_id = %s", (movie_id,))
                        
                        # Handle comma-separated genres
                        genres = [g.strip() for g in genres_text.split(',') if g.strip()]
                        for genre in genres:
                            execute_query(
                                "INSERT INTO movie_genres (movie_id, genre) VALUES (%s, %s)",
                                (movie_id, genre)
                            )
                    
                    if movie_result[0]['inserted']:
                        movies_added += 1
                    else:
                        movies_updated += 1
                        
            except Exception as e:
                errors.append(f"Row {row_num}: {str(e)}")
        
        return jsonify({
            'success': True,
            'movies_added': movies_added,
            'movies_updated': movies_updated,
            'errors': errors[:10],  # Limit errors to first 10
            'total_errors': len(errors)
        })
        
    except Exception as e:
        return jsonify({'error': f'CSV upload failed: {str(e)}'}), 500

def require_api_key(f):
    """Decorator to require API key for endpoints with rate limiting"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if not api_key:
            return jsonify({'error': 'API key required', 'message': 'Include X-API-Key header'}), 401
        
        user_info = AuthManager.validate_api_key(api_key)
        if not user_info:
            return jsonify({'error': 'Invalid API key'}), 401
        
        # Atomically check rate limit and increment usage
        try:
            check_and_increment_user_rate_limit(
                user_info['user_id'], 
                user_info['api_key_id'], 
                request.endpoint or 'unknown'
            )
        except RateLimitError as e:
            return jsonify({'error': str(e)}), 429
        except Exception as e:
            # Fail-closed: Return 503 if rate limiting service fails
            print(f"Rate limiting service error: {e}")
            return jsonify({
                'error': 'Rate limiting service temporarily unavailable',
                'message': 'Please try again later',
                'status': 'service_unavailable'
            }), 503
        
        # Add user info to request
        request.user_info = user_info
        
        # Execute the endpoint function
        result = f(*args, **kwargs)
        
        # Get current usage stats
        usage_stats = get_user_usage_stats(user_info['user_id'])
        
        # Handle different response types
        if isinstance(result, tuple) and len(result) == 2:
            response_data, status_code = result
        else:
            response_data = result
            status_code = 200
        
        # Extract JSON data from Flask Response objects
        response_json = None
        if hasattr(response_data, 'get_json'):
            # It's a Flask Response object
            response_json = response_data.get_json()
        elif isinstance(response_data, dict):
            # It's already a dict
            response_json = response_data.copy()
        
        # Add meta information if we have JSON data
        if response_json is not None:
            response_json['meta'] = {
                'user_email': user_info['email'],
                'plan': usage_stats.get('plan_type', 'free'),
                'usage': {
                    'used': usage_stats.get('daily_usage', 0),
                    'limit': usage_stats.get('daily_limit', 100),
                    'remaining': usage_stats.get('remaining_requests', 0)
                }
            }
            # Return new jsonify response with enhanced data
            return jsonify(response_json) if status_code == 200 else (jsonify(response_json), status_code)
        
        # Return original response if we can't enhance it
        return response_data if status_code == 200 else (response_data, status_code)
    return decorated_function

def require_api_key_no_limits(f):
    """Decorator for management endpoints that require API key but exempt from rate limiting"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if not api_key:
            return jsonify({'error': 'API key required', 'message': 'Include X-API-Key header'}), 401
        
        user_info = AuthManager.validate_api_key(api_key)
        if not user_info:
            return jsonify({'error': 'Invalid API key'}), 401
        
        # Add user info to request (no rate limiting or usage logging)
        request.user_info = user_info
        return f(*args, **kwargs)
    return decorated_function

@app.route('/admin/movies/<int:movie_id>', methods=['GET', 'PUT', 'DELETE'])
@require_firebase_admin
def admin_movie_detail(movie_id):
    """Admin endpoint for single movie CRUD operations"""
    if request.method == 'GET':
        try:
            movie = execute_query("""
                SELECT m.*, 
                       STRING_AGG(DISTINCT mg.genre, ', ') as genres,
                       STRING_AGG(DISTINCT CONCAT(c.actor_name, ' as ', c.role), '; ') as cast
                FROM movies m
                LEFT JOIN movie_genres mg ON m.id = mg.movie_id  
                LEFT JOIN movie_cast c ON m.id = c.movie_id
                WHERE m.id = %s
                GROUP BY m.id
            """, (movie_id,), fetch=True)
            
            if not movie:
                return jsonify({'error': 'Movie not found'}), 404
            
            return jsonify({'movie': movie[0]})
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    elif request.method == 'PUT':
        try:
            data = request.get_json()
            if not data:
                return jsonify({'error': 'No data provided'}), 400
            
            # Update movie
            execute_query("""
                UPDATE movies SET 
                    title = %s, year = %s, runtime = %s, rating = %s,
                    poster_url = %s, director = %s, plot = %s, external_id = %s
                WHERE id = %s
            """, (
                data.get('title'),
                data.get('year'),
                data.get('runtime'),
                data.get('rating'),
                data.get('poster_url'),
                data.get('director'),
                data.get('plot'),
                data.get('external_id'),
                movie_id
            ))
            
            return jsonify({'success': True, 'message': 'Movie updated successfully'})
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    elif request.method == 'DELETE':
        try:
            execute_query("DELETE FROM movies WHERE id = %s", (movie_id,))
            return jsonify({'success': True, 'message': 'Movie deleted successfully'})
        except Exception as e:
            return jsonify({'error': str(e)}), 500

@app.route('/')
def home():
    """API root endpoint"""
    return jsonify({
        'message': 'The Matrix Movie Database API',
        'version': '3.0',
        'authentication': 'API Key required (X-API-Key header)',
        'endpoints': {
            'movies': '/api/movies',
            'search': '/api/search',
            'stats': '/api/stats',
            'auth': '/auth/*'
        },
        'docs': 'Include X-API-Key header in all requests'
    })

# Authentication endpoints (no API key required)
@app.route('/auth/register', methods=['POST'])
def register():
    """Register new user"""
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({'error': 'Email and password required'}), 400
        
        result = AuthManager.create_user(email, password)
        return jsonify({
            'message': 'User created successfully',
            'api_key': result['api_key']
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/auth/login', methods=['POST'])
def login():
    """Login user"""
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        user = AuthManager.authenticate_user(email, password)
        if not user:
            return jsonify({'error': 'Invalid credentials'}), 401
        
        # Get user's API keys
        api_keys = AuthManager.get_user_api_keys(user['id'])
        
        return jsonify({
            'message': 'Login successful',
            'user': user,
            'api_keys': [key['api_key'] for key in api_keys if key['is_active']]
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/auth/dashboard/<int:user_id>', methods=['GET'])
def dashboard_stats(user_id):
    """Get dashboard statistics for user"""
    try:
        stats = AuthManager.get_usage_stats(user_id)
        api_keys = AuthManager.get_user_api_keys(user_id)
        
        return jsonify({
            'stats': stats,
            'api_keys': api_keys
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/auth/api-key/<int:user_id>', methods=['POST'])
def create_api_key(user_id):
    """Create new API key for user"""
    try:
        api_key = AuthManager.create_api_key(user_id)
        return jsonify({'api_key': api_key})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/auth/api-key/<int:user_id>/<int:key_id>', methods=['DELETE'])
def delete_api_key(user_id, key_id):
    """Delete API key"""
    try:
        AuthManager.delete_api_key(user_id, key_id)
        return jsonify({'message': 'API key deleted'})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/auth/account/<int:user_id>', methods=['DELETE'])
def delete_account(user_id):
    """Delete user account permanently"""
    try:
        AuthManager.delete_user_account(user_id)
        return jsonify({'message': 'Account deleted permanently'})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Protected movie endpoints (require API key)
@app.route('/api/movies', methods=['GET'])
@require_api_key
def get_movies():
    """Get all movies with optional filtering and pagination"""
    try:
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 20))
        genre = request.args.get('genre')
        year = request.args.get('year')
        search = request.args.get('search')
        
        offset = (page - 1) * limit
        
        query = """
            SELECT DISTINCT m.id, m.title, m.year, m.runtime, m.rating, 
                   m.director, m.plot, m.poster_url
            FROM movies m
        """
        
        conditions = []
        params = []
        
        if genre:
            query += " LEFT JOIN movie_genres mg ON m.id = mg.movie_id"
            conditions.append("mg.genre = %s")
            params.append(genre)
        
        if search:
            conditions.append("(m.title ILIKE %s OR m.director ILIKE %s OR m.plot ILIKE %s)")
            search_param = f"%{search}%"
            params.extend([search_param, search_param, search_param])
        
        if year:
            conditions.append("m.year = %s")
            params.append(int(year))
        
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        
        query += " ORDER BY m.year DESC, m.title LIMIT %s OFFSET %s"
        params.extend([limit, offset])
        
        movies = execute_query(query, tuple(params), fetch=True)
        
        # Enrich with genres and cast
        enriched_movies = []
        for movie in movies:
            movie_dict = dict(movie)
            
            genres_result = execute_query(
                "SELECT genre FROM movie_genres WHERE movie_id = %s ORDER BY genre",
                (movie['id'],), fetch=True
            )
            movie_dict['genres'] = [g['genre'] for g in genres_result]
            
            cast_result = execute_query(
                "SELECT actor_name FROM movie_cast WHERE movie_id = %s ORDER BY actor_name",
                (movie['id'],), fetch=True
            )
            movie_dict['cast'] = [c['actor_name'] for c in cast_result]
            
            enriched_movies.append(movie_dict)
        
        # Get total count
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
            },
            'user': request.user_info['email']
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/movies/<int:movie_id>', methods=['GET'])
@require_api_key
def get_movie(movie_id):
    """Get a specific movie by ID"""
    try:
        movie_result = execute_query(
            "SELECT * FROM movies WHERE id = %s",
            (movie_id,), fetch=True
        )
        
        if not movie_result:
            return jsonify({'error': 'Movie not found'}), 404
        
        movie = dict(movie_result[0])
        
        genres_result = execute_query(
            "SELECT genre FROM movie_genres WHERE movie_id = %s ORDER BY genre",
            (movie_id,), fetch=True
        )
        movie['genres'] = [g['genre'] for g in genres_result]
        
        cast_result = execute_query(
            "SELECT actor_name, role FROM movie_cast WHERE movie_id = %s ORDER BY actor_name",
            (movie_id,), fetch=True
        )
        movie['cast'] = [{'name': c['actor_name'], 'role': c['role']} for c in cast_result]
        
        return jsonify({
            'movie': movie,
            'user': request.user_info['email']
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/genres', methods=['GET'])
@require_api_key
def get_genres():
    """Get all available genres"""
    try:
        genres_result = execute_query(
            "SELECT DISTINCT genre FROM movie_genres ORDER BY genre",
            fetch=True
        )
        genres = [g['genre'] for g in genres_result]
        return jsonify({
            'genres': genres,
            'user': request.user_info['email']
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/years', methods=['GET'])
@require_api_key
def get_years():
    """Get all available years"""
    try:
        years_result = execute_query(
            "SELECT DISTINCT year FROM movies ORDER BY year DESC",
            fetch=True
        )
        years = [y['year'] for y in years_result]
        return jsonify({
            'years': years,
            'user': request.user_info['email']
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stats', methods=['GET'])
@require_api_key
def get_stats():
    """Get database statistics"""
    try:
        movies_count = execute_query("SELECT COUNT(*) as count FROM movies", fetch=True)[0]['count']
        genres_count = execute_query("SELECT COUNT(*) as count FROM movie_genres", fetch=True)[0]['count']
        cast_count = execute_query("SELECT COUNT(*) as count FROM movie_cast", fetch=True)[0]['count']
        
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
            },
            'user': request.user_info['email']
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/search', methods=['GET'])
@require_api_key
def search_movies():
    """Search movies by title, director, or plot"""
    try:
        query_param = request.args.get('q', '').strip()
        if not query_param:
            return jsonify({'error': 'Search query is required'}), 400
        
        search_param = f"%{query_param}%"
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
            'query': query_param,
            'count': len(enriched_movies),
            'user': request.user_info['email']
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/user/quota', methods=['GET'])
@require_api_key_no_limits
def get_user_quota():
    """Get user's current quota and usage stats"""
    try:
        user_id = request.user_info['user_id']
        stats = get_user_usage_stats(user_id)
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/user/upgrade', methods=['POST'])
@require_api_key_no_limits
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
    
    print("🚀 Starting Enhanced Movie Database API...")
    print("🔐 API Key Authentication Required")
    print("📊 Available endpoints:")
    print("  POST /auth/register       - Register new user")
    print("  POST /auth/login          - Login user")
    print("  GET  /auth/dashboard/{id} - Dashboard stats")
    print("  POST /auth/api-key/{id}   - Create API key")
    print("  DEL  /auth/api-key/{id}/{key_id} - Delete API key")
    print("  DEL  /auth/account/{id}   - Delete account")
    print("  GET  /api/movies          - List movies (API KEY REQUIRED)")
    print("  GET  /api/movies/{id}     - Get specific movie (API KEY REQUIRED)")
    print("  GET  /api/genres          - List all genres (API KEY REQUIRED)")
    print("  GET  /api/years           - List all years (API KEY REQUIRED)")
    print("  GET  /api/stats           - Database statistics (API KEY REQUIRED)")
    print("  GET  /api/search?q=term   - Search movies (API KEY REQUIRED)")
    
    app.run(host='0.0.0.0', port=8000, debug=True)