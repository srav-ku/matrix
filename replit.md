# Movie Database API with Modern UI

## Overview

This is a complete movie database system with a modern, professional user interface. The project features a **fully responsive React-like UI** built with modern web technologies, matching the exact design specifications provided. The system includes comprehensive movie data management, user authentication, and a professional dashboard interface.

## Project Status: ✅ FULLY OPERATIONAL IN REPLIT

The project has been successfully imported and configured to run in the Replit environment with both frontend and backend services fully operational. All dependencies installed, database populated with 50 movies, and both workflows running smoothly.

**Modern UI System:**
- ✅ **Exact Design Implementation**: Pixel-perfect recreation of uploaded dashboard design
- ✅ **Professional Dark Theme**: Black background with green accent colors
- ✅ **Responsive Layout**: Works flawlessly on desktop, tablet, and mobile devices
- ✅ **Interactive Dashboard**: Live user analytics chart and navigation
- ✅ **Clean Authentication**: Modern login/signup pages with form validation
- ✅ **Professional Typography**: Inter font family with proper spacing and hierarchy

**Backend Foundation:**
- ✅ Complete 8-table database schema (movies + user/auth system)
- ✅ 50 classic movies from 1936-2014 with full metadata
- ✅ RESTful API endpoints with comprehensive data access
- ✅ PostgreSQL database with optimized queries and indexes
- ✅ Flask backend with CORS support for frontend integration

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Technology**: Modern HTML5 + Tailwind CSS + JavaScript
- **Design System**: Professional dark theme with green accents
- **Layout**: Responsive flexbox layout with sidebar navigation
- **Components**: Modular glass-card components with backdrop blur effects
- **Interactivity**: Smooth hover states and click handlers
- **Charts**: SVG-based analytics visualization with gradient fills
- **Authentication**: Professional login/signup forms with validation

### Backend Architecture  
- **Technology**: Python Flask with PostgreSQL database
- **API Design**: RESTful endpoints for movie data and statistics
- **Database**: PostgreSQL with psycopg2 driver and connection pooling
- **Schema Design**: 8-table structure supporting both movie data and user management
  - Core movie tables: `movies`, `movie_genres`, `movie_cast`
  - User management tables: `users`, `email_verifications`, `api_keys`
  - Usage tracking tables: `usage_logs`, `daily_usage`
- **Data Relationships**: Many-to-many relationships for genres and cast members
- **Simplified API**: `simple_api.py` provides core movie functionality without authentication complexity

### Replit Environment Configuration
- **Frontend Workflow**: Next.js dev server running on port 5000 ✅ ACTIVE
- **Backend Workflow**: Flask API server running on port 8000 ✅ ACTIVE
- **Database**: Replit PostgreSQL instance with 50 imported movies ✅ POPULATED
- **Proxy Configuration**: Next.js configured to proxy API calls to backend
- **Host Configuration**: Both servers configured with allowedHosts for Replit's proxy environment
- **Deployment**: Configured for autoscale deployment with Next.js build process

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