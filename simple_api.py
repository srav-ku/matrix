#!/usr/bin/env python3
"""
Simple Movie Database API - Minimal version for Replit environment
RESTful API endpoints for the movie database
"""

import sys
import os
sys.path.append('.')
sys.path.append('./src')

from flask import Flask, jsonify, request
from flask_cors import CORS
from src.database import execute_query

app = Flask(__name__)

# Configure CORS for Replit environment - allow all origins for development
CORS(app, origins="*")

# Configure Flask for development
app.config['DEBUG'] = True

# Essential for Replit: Disable host header checks for proxy environments
app.config['SERVER_NAME'] = None

@app.route('/')
def home():
    """API root endpoint"""
    return jsonify({
        'message': 'Movie Database API',
        'version': '2.0',
        'endpoints': {
            'movies': '/api/movies',
            'search': '/api/search',
            'stats': '/api/stats'
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
            'count': len(enriched_movies)
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
    print("  GET /                     - API info")
    print("  GET /api/movies          - List movies (with pagination & filters)")
    print("  GET /api/movies/{id}     - Get specific movie")
    print("  GET /api/genres          - List all genres")
    print("  GET /api/years           - List all years")
    print("  GET /api/stats           - Database statistics")
    print("  GET /api/search?q=term   - Search movies")
    
    # Start the server on all interfaces for Replit
    app.run(host='0.0.0.0', port=8000, debug=True)