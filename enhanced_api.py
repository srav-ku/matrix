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

app = Flask(__name__)

# Configure CORS for Replit environment
CORS(app, origins="*")

# Configure Flask for development
app.config['DEBUG'] = True
app.config['SERVER_NAME'] = None

def require_api_key(f):
    """Decorator to require API key for endpoints"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if not api_key:
            return jsonify({'error': 'API key required', 'message': 'Include X-API-Key header'}), 401
        
        user_info = AuthManager.validate_api_key(api_key)
        if not user_info:
            return jsonify({'error': 'Invalid API key'}), 401
        
        # Log usage
        AuthManager.log_api_usage(user_info['api_key_id'], request.endpoint, 200)
        
        # Add user info to request
        request.user_info = user_info
        return f(*args, **kwargs)
    return decorated_function

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