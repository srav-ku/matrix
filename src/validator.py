import csv
import re
from datetime import datetime
from typing import List, Dict, Tuple, Any

class MovieCSVValidator:
    """Validates movie CSV files according to Phase 1 requirements"""
    
    REQUIRED_FIELDS = ['title', 'year', 'genre', 'runtime']
    VALID_GENRES = {
        'Action', 'Adventure', 'Animation', 'Biography', 'Comedy', 'Crime', 
        'Documentary', 'Drama', 'Family', 'Fantasy', 'Film-Noir', 'History', 
        'Horror', 'Music', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 
        'Sport', 'Thriller', 'War', 'Western'
    }
    
    MIN_YEAR = 1900
    MAX_YEAR = 2025
    MIN_RUNTIME = 1
    MAX_RATING = 10.0
    MIN_RATING = 0.0
    
    def __init__(self):
        self.errors = []
        self.warnings = []
        
    def validate_csv_file(self, csv_file_path: str) -> Dict[str, Any]:
        """Validate entire CSV file and return comprehensive report"""
        self.errors = []
        self.warnings = []
        
        try:
            with open(csv_file_path, 'r', encoding='utf-8') as file:
                # Check if file is empty
                content = file.read().strip()
                if not content:
                    self.errors.append("CSV file is empty")
                    return self._generate_report(0, 0)
                
                file.seek(0)  # Reset file pointer
                csv_reader = csv.DictReader(file)
                
                # Validate headers
                headers = csv_reader.fieldnames
                if not headers:
                    self.errors.append("CSV file has no headers")
                    return self._generate_report(0, 0)
                
                self._validate_headers(headers)
                
                # Validate each row
                valid_rows = 0
                total_rows = 0
                duplicate_check = set()
                
                for row_num, row in enumerate(csv_reader, start=2):  # Start at 2 (after header)
                    total_rows += 1
                    row_errors = self._validate_row(row, row_num)
                    
                    # Check for duplicates (title + year combination)
                    if 'title' in row and 'year' in row:
                        duplicate_key = (row['title'].strip().lower(), row['year'].strip())
                        if duplicate_key in duplicate_check:
                            row_errors.append(f"Duplicate movie: {row['title']} ({row['year']})")
                        else:
                            duplicate_check.add(duplicate_key)
                    
                    if not row_errors:
                        valid_rows += 1
                    else:
                        for error in row_errors:
                            self.errors.append(f"Row {row_num}: {error}")
                
                return self._generate_report(total_rows, valid_rows)
                
        except FileNotFoundError:
            self.errors.append(f"File not found: {csv_file_path}")
            return self._generate_report(0, 0)
        except Exception as e:
            self.errors.append(f"Error reading CSV file: {str(e)}")
            return self._generate_report(0, 0)
    
    def _validate_headers(self, headers: List[str]) -> None:
        """Validate CSV headers"""
        if not headers:
            self.errors.append("No headers found in CSV file")
            return
        
        # Check for required fields
        missing_required = []
        for field in self.REQUIRED_FIELDS:
            if field not in headers:
                missing_required.append(field)
        
        if missing_required:
            self.errors.append(f"Missing required headers: {', '.join(missing_required)}")
        
        # Check for unexpected empty headers
        if '' in headers or None in headers:
            self.errors.append("Empty header column found")
    
    def _validate_row(self, row: Dict[str, str], row_num: int) -> List[str]:
        """Validate a single row and return list of errors"""
        row_errors = []
        
        # Check required fields are not empty
        for field in self.REQUIRED_FIELDS:
            if field not in row or not row[field] or not row[field].strip():
                row_errors.append(f"Required field '{field}' is missing or empty")
        
        # Validate title
        if 'title' in row and row['title']:
            title = row['title'].strip()
            if len(title) > 500:
                row_errors.append(f"Title too long (max 500 characters): {len(title)} characters")
            if len(title) < 1:
                row_errors.append("Title cannot be empty")
        
        # Validate year
        if 'year' in row and row['year']:
            try:
                year = int(row['year'].strip())
                if year < self.MIN_YEAR or year > self.MAX_YEAR:
                    row_errors.append(f"Year {year} out of valid range ({self.MIN_YEAR}-{self.MAX_YEAR})")
            except ValueError:
                row_errors.append(f"Invalid year format: '{row['year']}'")
        
        # Validate runtime
        if 'runtime' in row and row['runtime']:
            try:
                runtime = int(row['runtime'].strip())
                if runtime <= 0:
                    row_errors.append(f"Runtime must be greater than 0: {runtime}")
            except ValueError:
                row_errors.append(f"Invalid runtime format: '{row['runtime']}'")
        
        # Validate genre
        if 'genre' in row and row['genre']:
            genres = [g.strip() for g in row['genre'].split('|') if g.strip()]
            invalid_genres = []
            for genre in genres:
                if genre not in self.VALID_GENRES:
                    invalid_genres.append(genre)
            if invalid_genres:
                row_errors.append(f"Invalid genres: {', '.join(invalid_genres)}")
            if not genres:
                row_errors.append("At least one valid genre is required")
        
        # Validate rating (optional field)
        if 'rating' in row and row['rating'] and row['rating'].strip():
            try:
                rating = float(row['rating'].strip())
                if rating < self.MIN_RATING or rating > self.MAX_RATING:
                    row_errors.append(f"Rating {rating} out of valid range ({self.MIN_RATING}-{self.MAX_RATING})")
            except ValueError:
                row_errors.append(f"Invalid rating format: '{row['rating']}'")
        
        # Validate poster URL (optional field)
        if 'poster_url' in row and row['poster_url'] and row['poster_url'].strip():
            url = row['poster_url'].strip()
            if not self._is_valid_url(url):
                row_errors.append(f"Invalid poster URL format: {url}")
        
        return row_errors
    
    def _is_valid_url(self, url: str) -> bool:
        """Basic URL validation"""
        url_pattern = re.compile(
            r'^https?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        return url_pattern.match(url) is not None
    
    def _generate_report(self, total_rows: int, valid_rows: int) -> Dict[str, Any]:
        """Generate validation report"""
        return {
            'is_valid': len(self.errors) == 0,
            'total_rows': total_rows,
            'valid_rows': valid_rows,
            'invalid_rows': total_rows - valid_rows,
            'errors': self.errors.copy(),
            'warnings': self.warnings.copy(),
            'summary': f"{valid_rows}/{total_rows} rows valid" if total_rows > 0 else "No rows found"
        }
    
    def print_report(self, report: Dict[str, Any]) -> None:
        """Print a formatted validation report"""
        print("\n" + "="*60)
        print("CSV VALIDATION REPORT")
        print("="*60)
        
        if report['is_valid']:
            print("✅ VALIDATION PASSED")
        else:
            print("❌ VALIDATION FAILED")
        
        print(f"\nSummary: {report['summary']}")
        print(f"Total rows: {report['total_rows']}")
        print(f"Valid rows: {report['valid_rows']}")
        print(f"Invalid rows: {report['invalid_rows']}")
        
        if report['errors']:
            print(f"\n❌ ERRORS ({len(report['errors'])}):")
            for error in report['errors']:
                print(f"  • {error}")
        
        if report['warnings']:
            print(f"\n⚠️  WARNINGS ({len(report['warnings'])}):")
            for warning in report['warnings']:
                print(f"  • {warning}")
        
        print("="*60)

def validate_csv_file(csv_path: str) -> Dict[str, Any]:
    """Convenience function to validate a CSV file"""
    validator = MovieCSVValidator()
    return validator.validate_csv_file(csv_path)

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python validator.py <csv_file_path>")
        sys.exit(1)
    
    csv_path = sys.argv[1]
    validator = MovieCSVValidator()
    report = validator.validate_csv_file(csv_path)
    validator.print_report(report)
    
    # Exit with error code if validation failed
    sys.exit(0 if report['is_valid'] else 1)