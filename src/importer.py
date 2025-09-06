import csv
import sys
from typing import Dict, List, Any, Tuple, Optional
from datetime import datetime
from database import execute_query, get_db_connection
from validator import MovieCSVValidator

class MovieCSVImporter:
    """Idempotent CSV importer for movies with dry-run support"""
    
    def __init__(self):
        self.validator = MovieCSVValidator()
        self.import_stats = {
            'total_processed': 0,
            'inserted': 0,
            'updated': 0,
            'skipped': 0,
            'errors': []
        }
    
    def import_csv(self, csv_file_path: str, dry_run: bool = False) -> Dict[str, Any]:
        """
        Import movies from CSV file with idempotent behavior
        
        Args:
            csv_file_path: Path to the CSV file
            dry_run: If True, validate and show what would happen without importing
            
        Returns:
            Import report dictionary
        """
        print(f"\n{'DRY RUN' if dry_run else 'IMPORT'} MODE: Processing {csv_file_path}")
        print("="*60)
        
        # Reset stats
        self.import_stats = {
            'total_processed': 0,
            'inserted': 0,
            'updated': 0,
            'skipped': 0,
            'errors': []
        }
        
        # First validate the CSV
        validation_report = self.validator.validate_csv_file(csv_file_path)
        
        if not validation_report['is_valid']:
            print("❌ CSV validation failed. Cannot proceed with import.")
            self.validator.print_report(validation_report)
            return {
                'success': False,
                'validation_report': validation_report,
                'import_stats': self.import_stats,
                'dry_run': dry_run
            }
        
        print("✅ CSV validation passed. Proceeding with import...")
        
        try:
            with open(csv_file_path, 'r', encoding='utf-8') as file:
                csv_reader = csv.DictReader(file)
                
                for row_num, row in enumerate(csv_reader, start=1):
                    self.import_stats['total_processed'] += 1
                    
                    try:
                        if dry_run:
                            action = self._determine_action(row)
                            print(f"Row {row_num}: Would {action} - {row['title']} ({row['year']})")
                        else:
                            action = self._import_movie_row(row)
                            print(f"Row {row_num}: {action} - {row['title']} ({row['year']})")
                            
                    except Exception as e:
                        error_msg = f"Row {row_num}: Error processing {row.get('title', 'Unknown')}: {str(e)}"
                        self.import_stats['errors'].append(error_msg)
                        print(f"❌ {error_msg}")
        
        except Exception as e:
            error_msg = f"Error reading CSV file: {str(e)}"
            self.import_stats['errors'].append(error_msg)
            print(f"❌ {error_msg}")
            return {
                'success': False,
                'validation_report': validation_report,
                'import_stats': self.import_stats,
                'dry_run': dry_run
            }
        
        # Generate final report
        success = len(self.import_stats['errors']) == 0
        self._print_import_report(dry_run)
        
        return {
            'success': success,
            'validation_report': validation_report,
            'import_stats': self.import_stats,
            'dry_run': dry_run
        }
    
    def _determine_action(self, row: Dict[str, str]) -> str:
        """Determine what action would be taken for this row (for dry-run)"""
        title = row['title'].strip()
        year = int(row['year'].strip())
        
        # Check if movie exists
        existing_movie = self._get_existing_movie(title, year)
        
        if existing_movie:
            return "UPDATE"
        else:
            return "INSERT"
    
    def _import_movie_row(self, row: Dict[str, str]) -> str:
        """Import a single movie row, handling insert/update logic"""
        title = row['title'].strip()
        year = int(row['year'].strip())
        runtime = int(row['runtime'].strip())
        rating = float(row['rating'].strip()) if row.get('rating') and row['rating'].strip() else None
        director = row.get('director', '').strip() or None
        plot = row.get('plot', '').strip() or None
        poster_url = row.get('poster_url', '').strip() or None
        
        # Check if movie already exists (using title + year as natural key)
        existing_movie = self._get_existing_movie(title, year)
        
        if existing_movie:
            # Update existing movie
            movie_id = self._update_movie(existing_movie['id'], {
                'runtime': runtime,
                'rating': rating,
                'director': director,
                'plot': plot,
                'poster_url': poster_url
            })
            action = "UPDATED"
            self.import_stats['updated'] += 1
        else:
            # Insert new movie
            movie_id = self._insert_movie({
                'title': title,
                'year': year,
                'runtime': runtime,
                'rating': rating,
                'director': director,
                'plot': plot,
                'poster_url': poster_url
            })
            action = "INSERTED"
            self.import_stats['inserted'] += 1
        
        # Handle genres
        if row.get('genre'):
            genres = [g.strip() for g in row['genre'].split('|') if g.strip()]
            self._update_movie_genres(movie_id, genres)
        
        # Handle actors
        if row.get('actors'):
            actors = [a.strip() for a in row['actors'].split('|') if a.strip()]
            self._update_movie_cast(movie_id, actors)
        
        return action
    
    def _get_existing_movie(self, title: str, year: int) -> Optional[Dict]:
        """Get existing movie by title and year"""
        query = "SELECT id, title, year FROM movies WHERE title = %s AND year = %s"
        result = execute_query(query, (title, year), fetch=True)
        return result[0] if result else None
    
    def _insert_movie(self, movie_data: Dict[str, Any]) -> int:
        """Insert a new movie and return its ID"""
        query = """
        INSERT INTO movies (title, year, runtime, rating, director, plot, poster_url)
        VALUES (%(title)s, %(year)s, %(runtime)s, %(rating)s, %(director)s, %(plot)s, %(poster_url)s)
        RETURNING id
        """
        
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, movie_data)
                movie_id = cursor.fetchone()[0]
                conn.commit()
                return movie_id
    
    def _update_movie(self, movie_id: int, movie_data: Dict[str, Any]) -> int:
        """Update existing movie"""
        query = """
        UPDATE movies 
        SET runtime = %(runtime)s, rating = %(rating)s, director = %(director)s, 
            plot = %(plot)s, poster_url = %(poster_url)s
        WHERE id = %(id)s
        """
        movie_data['id'] = movie_id
        execute_query(query, movie_data)
        return movie_id
    
    def _update_movie_genres(self, movie_id: int, genres: List[str]) -> None:
        """Update movie genres (replace existing)"""
        # Delete existing genres
        execute_query("DELETE FROM movie_genres WHERE movie_id = %s", (movie_id,))
        
        # Insert new genres
        for genre in genres:
            execute_query(
                "INSERT INTO movie_genres (movie_id, genre) VALUES (%s, %s)",
                (movie_id, genre)
            )
    
    def _update_movie_cast(self, movie_id: int, actors: List[str]) -> None:
        """Update movie cast (replace existing)"""
        # Delete existing cast
        execute_query("DELETE FROM movie_cast WHERE movie_id = %s", (movie_id,))
        
        # Insert new cast
        for actor in actors:
            execute_query(
                "INSERT INTO movie_cast (movie_id, actor_name, role) VALUES (%s, %s, %s)",
                (movie_id, actor, None)  # Role is optional for now
            )
    
    def _print_import_report(self, dry_run: bool) -> None:
        """Print import statistics report"""
        mode = "DRY RUN" if dry_run else "IMPORT"
        print(f"\n{'='*60}")
        print(f"{mode} REPORT")
        print("="*60)
        
        print(f"Total rows processed: {self.import_stats['total_processed']}")
        if dry_run:
            would_insert = sum(1 for _ in range(self.import_stats['total_processed'])) - self.import_stats['updated']
            print(f"Would insert: {would_insert}")
            print(f"Would update: {self.import_stats['updated']}")
        else:
            print(f"Inserted: {self.import_stats['inserted']}")
            print(f"Updated: {self.import_stats['updated']}")
            print(f"Skipped: {self.import_stats['skipped']}")
        
        if self.import_stats['errors']:
            print(f"\n❌ ERRORS ({len(self.import_stats['errors'])}):")
            for error in self.import_stats['errors']:
                print(f"  • {error}")
        else:
            print(f"\n✅ {mode} completed successfully!")
        
        print("="*60)

def main():
    """Main function for command-line usage"""
    if len(sys.argv) < 2:
        print("Usage: python importer.py <csv_file> [--dry-run]")
        print("\nOptions:")
        print("  --dry-run    Validate and show what would happen without importing")
        sys.exit(1)
    
    csv_file = sys.argv[1]
    dry_run = '--dry-run' in sys.argv
    
    importer = MovieCSVImporter()
    result = importer.import_csv(csv_file, dry_run=dry_run)
    
    # Exit with error code if import failed
    sys.exit(0 if result['success'] else 1)

if __name__ == "__main__":
    main()