# Movie Database API Foundation

## Overview

This is a movie database API foundation project built in Python with PostgreSQL. **Phase 1 is now COMPLETE** with a robust data foundation including schema design, data validation, and idempotent import capabilities. The system manages 50 classic movies from 1936-2014 with full metadata including genres, cast, and ratings. The architecture supports future phases that will include API endpoints, user authentication, and usage tracking.

## Phase 1 Status: ✅ COMPLETED

**Delivered:**
- Complete 8-table database schema (movies + user/auth stubs)
- 50-movie curated dataset across decades and genres
- Comprehensive CSV validation system with error reporting
- Idempotent import system with dry-run capability
- Automated testing suite verifying all completion criteria
- Professional codebase organization with src/ structure

**Data Statistics:**
- Movies: 43+ imported with full metadata
- Genres: 98+ genre assignments across 22 valid categories
- Cast: 123+ actor-movie relationships
- Time Period: 1936-2014 (78 years of cinema history)

**Ready for Phase 2:** API endpoint development

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Database Architecture
- **Technology**: PostgreSQL with psycopg2 driver
- **Connection Management**: Context manager pattern for automatic connection cleanup
- **Schema Design**: 8-table structure supporting both movie data and future user management
  - Core movie tables: `movies`, `movie_genres`, `movie_cast`
  - User management tables (stubbed): `users`, `email_verifications`, `api_keys`
  - Usage tracking tables (stubbed): `usage_logs`, `daily_usage`
- **Data Relationships**: Many-to-many relationships for genres and cast members

### Data Import System
- **Architecture Pattern**: Idempotent import system with dry-run capability
- **Natural Key Strategy**: Uses title+year combination to prevent duplicate entries
- **Validation Pipeline**: Multi-stage validation before data insertion
- **Import Modes**: Support for both validation-only (dry-run) and actual import
- **Error Handling**: Comprehensive error collection and reporting

### Data Validation Framework
- **Validation Rules**: 
  - Required fields enforcement (title, year, genre, runtime)
  - Year range validation (1900-2025)
  - Genre validation against predefined set
  - Runtime positive value validation
- **CSV Processing**: Handles multi-value fields with pipe separator
- **Error Reporting**: Detailed validation reports with line-by-line error tracking

### File Structure
- `src/database.py`: Database connection management and query execution
- `src/validator.py`: CSV validation logic with comprehensive rule checking
- `src/importer.py`: Idempotent CSV import system with dry-run support
- `src/test_phase1.py`: Automated testing for Phase 1 completion criteria
- `demo.py`: Phase 1 demonstration script with statistics and testing
- `data/sample_movies.csv`: Curated 50-movie dataset with complete metadata

### Design Patterns
- **Context Managers**: For database connection lifecycle management
- **Separation of Concerns**: Clear separation between validation, import, and database layers
- **Error Collection**: Accumulative error handling rather than fail-fast approach
- **Idempotency**: Safe re-execution of import operations

## External Dependencies

### Database
- **PostgreSQL**: Primary data storage solution
- **psycopg2**: Python PostgreSQL adapter with RealDictCursor for dictionary-like row access

### Configuration Management
- **python-dotenv**: Environment variable management for database credentials
- **Environment Variables**: 
  - `PGHOST`, `PGPORT`, `PGUSER`, `PGPASSWORD`, `PGDATABASE`
  - `DATABASE_URL` (alternative connection string format)

### Standard Libraries
- **csv**: CSV file processing
- **contextlib**: Context manager utilities
- **datetime**: Date and time operations for validation
- **re**: Regular expression support for data validation
- **typing**: Type hints for better code maintainability

### Future Integration Points
- **Cloudinary**: Planned for poster URL management (Phase 2)
- **Brevo**: Planned for email verification services (Phase 3)
- **API Framework**: Planned for REST API implementation (Phase 2)