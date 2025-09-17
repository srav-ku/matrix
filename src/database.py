import os
import psycopg2
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager
from dotenv import load_dotenv

load_dotenv()

# Database connection parameters
DATABASE_URL = os.getenv('DATABASE_URL')
PGHOST = os.getenv('PGHOST')
PGPORT = os.getenv('PGPORT')
PGUSER = os.getenv('PGUSER')
PGPASSWORD = os.getenv('PGPASSWORD')
PGDATABASE = os.getenv('PGDATABASE')

@contextmanager
def get_db_connection():
    """Context manager for database connections"""
    conn = None
    try:
        conn = psycopg2.connect(
            host=PGHOST,
            port=PGPORT,
            user=PGUSER,
            password=PGPASSWORD,
            database=PGDATABASE
        )
        yield conn
    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn:
            conn.close()

def execute_query(query, params=None, fetch=False):
    """Execute a query and optionally fetch results"""
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query, params)
            if fetch:
                result = cursor.fetchall()
                conn.commit()
                return result
            conn.commit()
            return cursor.rowcount

def execute_transaction(queries):
    """Execute multiple queries in a single transaction"""
    with get_db_connection() as conn:
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                results = []
                for query, params, fetch in queries:
                    cursor.execute(query, params)
                    if fetch:
                        results.append(cursor.fetchall())
                    else:
                        results.append(cursor.rowcount)
                conn.commit()
                return results
        except Exception as e:
            conn.rollback()
            raise e

def create_schema():
    """Create all database tables for Phase 1"""
    
    # Drop tables if they exist (for clean setup)
    drop_tables_sql = """
    DROP TABLE IF EXISTS rate_limits CASCADE;
    DROP TABLE IF EXISTS user_subscriptions CASCADE;
    DROP TABLE IF EXISTS daily_usage CASCADE;
    DROP TABLE IF EXISTS usage_logs CASCADE;
    DROP TABLE IF EXISTS api_keys CASCADE;
    DROP TABLE IF EXISTS email_verifications CASCADE;
    DROP TABLE IF EXISTS movie_cast CASCADE;
    DROP TABLE IF EXISTS movie_genres CASCADE;
    DROP TABLE IF EXISTS movies CASCADE;
    DROP TABLE IF EXISTS users CASCADE;
    """
    
    # Create tables schema
    create_tables_sql = """
    -- Users table (stub for Phase 3)
    CREATE TABLE users (
        id SERIAL PRIMARY KEY,
        email VARCHAR(255) UNIQUE NOT NULL,
        password_hash VARCHAR(255) NOT NULL,
        is_verified BOOLEAN DEFAULT FALSE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    
    -- Email verifications table (stub for Phase 3)
    CREATE TABLE email_verifications (
        id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
        otp_code VARCHAR(10) NOT NULL,
        expiry TIMESTAMP NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    
    -- API keys table (stub for Phase 3)
    CREATE TABLE api_keys (
        id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
        api_key VARCHAR(255) UNIQUE NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        is_active BOOLEAN DEFAULT TRUE
    );
    
    -- Movies table (main data for Phase 1)
    CREATE TABLE movies (
        id SERIAL PRIMARY KEY,
        title VARCHAR(500) NOT NULL,
        year INTEGER NOT NULL,
        runtime INTEGER NOT NULL CHECK (runtime > 0),
        rating DECIMAL(3,1) CHECK (rating >= 0 AND rating <= 10),
        poster_url TEXT,
        director VARCHAR(255),
        plot TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(title, year)
    );
    
    -- Movie genres table (many-to-many)
    CREATE TABLE movie_genres (
        id SERIAL PRIMARY KEY,
        movie_id INTEGER REFERENCES movies(id) ON DELETE CASCADE,
        genre VARCHAR(100) NOT NULL,
        UNIQUE(movie_id, genre)
    );
    
    -- Movie cast table (many-to-many)
    CREATE TABLE movie_cast (
        id SERIAL PRIMARY KEY,
        movie_id INTEGER REFERENCES movies(id) ON DELETE CASCADE,
        actor_name VARCHAR(255) NOT NULL,
        role VARCHAR(255),
        UNIQUE(movie_id, actor_name, role)
    );
    
    -- Usage logs table (stub for Phase 3)
    CREATE TABLE usage_logs (
        id SERIAL PRIMARY KEY,
        api_key_id INTEGER REFERENCES api_keys(id) ON DELETE CASCADE,
        endpoint VARCHAR(255) NOT NULL,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        status_code INTEGER NOT NULL
    );
    
    -- Daily usage table (stub for Phase 3)
    CREATE TABLE daily_usage (
        id SERIAL PRIMARY KEY,
        api_key_id INTEGER REFERENCES api_keys(id) ON DELETE CASCADE,
        date DATE NOT NULL,
        request_count INTEGER DEFAULT 0,
        UNIQUE(api_key_id, date)
    );

    -- User subscriptions table for plan management
    CREATE TABLE user_subscriptions (
        id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES users(id) ON DELETE CASCADE UNIQUE,
        plan_type VARCHAR(20) DEFAULT 'free' CHECK (plan_type IN ('free', 'premium')),
        daily_limit INTEGER DEFAULT 100,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    -- Rate limiting table for general rate limiting
    CREATE TABLE rate_limits (
        id SERIAL PRIMARY KEY,
        identifier VARCHAR(255) NOT NULL,
        action VARCHAR(100) NOT NULL,
        timestamp INTEGER NOT NULL
    );
    
    -- Create indexes for performance
    CREATE INDEX idx_movies_year ON movies(year);
    CREATE INDEX idx_movies_title ON movies(title);
    CREATE INDEX idx_movie_genres_movie_id ON movie_genres(movie_id);
    CREATE INDEX idx_movie_cast_movie_id ON movie_cast(movie_id);
    CREATE INDEX idx_usage_logs_timestamp ON usage_logs(timestamp);
    CREATE INDEX idx_daily_usage_date ON daily_usage(date);
    CREATE INDEX idx_user_subscriptions_user_id ON user_subscriptions(user_id);
    CREATE INDEX idx_rate_limits_identifier_action ON rate_limits(identifier, action);
    CREATE INDEX idx_rate_limits_timestamp ON rate_limits(timestamp);
    """
    
    print("Creating database schema...")
    try:
        execute_query(drop_tables_sql)
        execute_query(create_tables_sql)
        print("✅ Database schema created successfully!")
        
        # Verify tables were created
        tables_query = """
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public'
        ORDER BY table_name;
        """
        tables = execute_query(tables_query, fetch=True)
        print(f"✅ Created {len(tables)} tables:")
        for table in tables:
            print(f"  - {table['table_name']}")
            
    except Exception as e:
        print(f"❌ Error creating schema: {e}")
        raise

if __name__ == "__main__":
    create_schema()