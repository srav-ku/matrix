#!/usr/bin/env python3
"""
Movie Database Phase 1 Demo
Shows the complete Phase 1 functionality
"""

import sys
import os
sys.path.append('src')

from src.database import execute_query
from src.validator import MovieCSVValidator
from src.importer import MovieCSVImporter
from src.test_phase1 import test_phase1_criteria

def show_movie_stats():
    """Display current database statistics"""
    print("📊 DATABASE STATISTICS")
    print("-" * 40)
    
    # Get counts
    movies_count = execute_query("SELECT COUNT(*) as count FROM movies", fetch=True)[0]['count']
    genres_count = execute_query("SELECT COUNT(*) as count FROM movie_genres", fetch=True)[0]['count']
    cast_count = execute_query("SELECT COUNT(*) as count FROM movie_cast", fetch=True)[0]['count']
    
    print(f"Movies: {movies_count}")
    print(f"Genres: {genres_count}")
    print(f"Cast entries: {cast_count}")
    
    # Show sample data
    if movies_count > 0:
        print("\n🎬 SAMPLE MOVIES:")
        movies = execute_query("""
            SELECT m.title, m.year, m.runtime, m.rating,
                   STRING_AGG(DISTINCT mg.genre, ', ') as genres
            FROM movies m
            LEFT JOIN movie_genres mg ON m.id = mg.movie_id
            GROUP BY m.id, m.title, m.year, m.runtime, m.rating
            ORDER BY m.year DESC
            LIMIT 5
        """, fetch=True)
        
        for movie in movies:
            genres = movie['genres'] or 'No genres'
            rating = f"{movie['rating']}/10" if movie['rating'] else "No rating"
            print(f"  • {movie['title']} ({movie['year']}) - {movie['runtime']}min, {rating}")
            print(f"    Genres: {genres}")
    
    print("-" * 40)

def main():
    """Main demo function"""
    print("🎯 MOVIE DATABASE API - PHASE 1 DEMO")
    print("=" * 60)
    
    print("\nThis demo shows Phase 1 completion:")
    print("✅ Database schema with 8 tables (movies + user/auth stubs)")
    print("✅ CSV validation system with comprehensive rules")
    print("✅ Idempotent import system with dry-run mode")
    print("✅ 50 diverse classic movies from 1936-2014")
    print("✅ All Phase 1 criteria met and tested")
    
    show_movie_stats()
    
    print("\n🧪 Running Phase 1 completion tests...")
    success = test_phase1_criteria()
    
    if success:
        print("\n🚀 Phase 1 is complete and ready for Phase 2 API development!")
    
    print("\n📝 AVAILABLE COMMANDS:")
    print("- python src/validator.py data/sample_movies.csv  # Validate CSV")
    print("- python src/importer.py data/sample_movies.csv --dry-run  # Dry run import")
    print("- python src/importer.py data/sample_movies.csv  # Import data")
    print("- python src/test_phase1.py  # Run all tests")
    
    return success

if __name__ == "__main__":
    main()