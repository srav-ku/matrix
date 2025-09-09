#!/usr/bin/env python3
"""
Authentication and API Key Management System
"""

import os
import secrets
import hashlib
from datetime import datetime, timedelta
from database import execute_query

class AuthManager:
    """Handle user authentication and API key management"""
    
    @staticmethod
    def generate_api_key():
        """Generate a secure API key"""
        return f"mk_{secrets.token_urlsafe(32)}"
    
    @staticmethod
    def hash_password(password):
        """Hash a password"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    @staticmethod
    def create_user(email, password):
        """Create a new user"""
        try:
            password_hash = AuthManager.hash_password(password)
            
            # First create the user
            user_result = execute_query(
                "INSERT INTO users (email, password_hash, is_verified) VALUES (%s, %s, TRUE) RETURNING id",
                (email, password_hash),
                fetch=True
            )
            
            if not user_result:
                raise Exception("Failed to create user")
                
            user_id = user_result[0]['id']
            
            # Then generate default API key
            api_key = AuthManager.generate_api_key()
            execute_query(
                "INSERT INTO api_keys (user_id, api_key) VALUES (%s, %s)",
                (user_id, api_key)
            )
            
            return {'user_id': user_id, 'api_key': api_key}
        except Exception as e:
            raise Exception(f"User creation failed: {str(e)}")
    
    @staticmethod
    def authenticate_user(email, password):
        """Authenticate user login"""
        try:
            password_hash = AuthManager.hash_password(password)
            user = execute_query(
                "SELECT id, email FROM users WHERE email = %s AND password_hash = %s AND is_verified = TRUE",
                (email, password_hash),
                fetch=True
            )
            
            if user:
                return user[0]
            return None
        except Exception:
            return None
    
    @staticmethod
    def get_user_api_keys(user_id):
        """Get all API keys for a user"""
        return execute_query(
            "SELECT id, api_key, created_at, is_active FROM api_keys WHERE user_id = %s ORDER BY created_at DESC",
            (user_id,),
            fetch=True
        )
    
    @staticmethod
    def create_api_key(user_id):
        """Create a new API key for user"""
        api_key = AuthManager.generate_api_key()
        execute_query(
            "INSERT INTO api_keys (user_id, api_key) VALUES (%s, %s)",
            (user_id, api_key)
        )
        return api_key
    
    @staticmethod
    def validate_api_key(api_key):
        """Validate API key and return user info"""
        result = execute_query(
            """SELECT ak.id as api_key_id, ak.user_id, u.email 
               FROM api_keys ak 
               JOIN users u ON ak.user_id = u.id 
               WHERE ak.api_key = %s AND ak.is_active = TRUE AND u.is_verified = TRUE""",
            (api_key,),
            fetch=True
        )
        return result[0] if result else None
    
    @staticmethod
    def log_api_usage(api_key_id, endpoint, status_code):
        """Log API usage"""
        execute_query(
            "INSERT INTO usage_logs (api_key_id, endpoint, status_code) VALUES (%s, %s, %s)",
            (api_key_id, endpoint, status_code)
        )
        
        # Update daily usage
        today = datetime.now().date()
        execute_query(
            """INSERT INTO daily_usage (api_key_id, date, request_count) 
               VALUES (%s, %s, 1) 
               ON CONFLICT (api_key_id, date) 
               DO UPDATE SET request_count = daily_usage.request_count + 1""",
            (api_key_id, today)
        )
    
    @staticmethod
    def get_usage_stats(user_id):
        """Get usage statistics for a user"""
        # Total requests
        total_requests = execute_query(
            """SELECT COUNT(*) as count FROM usage_logs ul 
               JOIN api_keys ak ON ul.api_key_id = ak.id 
               WHERE ak.user_id = %s""",
            (user_id,),
            fetch=True
        )[0]['count']
        
        # This month requests
        this_month_start = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        this_month_requests = execute_query(
            """SELECT COUNT(*) as count FROM usage_logs ul 
               JOIN api_keys ak ON ul.api_key_id = ak.id 
               WHERE ak.user_id = %s AND ul.timestamp >= %s""",
            (user_id, this_month_start),
            fetch=True
        )[0]['count']
        
        # API key count
        api_key_count = execute_query(
            "SELECT COUNT(*) as count FROM api_keys WHERE user_id = %s AND is_active = TRUE",
            (user_id,),
            fetch=True
        )[0]['count']
        
        # Last 24 hours usage for chart
        chart_data = execute_query(
            """SELECT EXTRACT(HOUR FROM ul.timestamp) as hour, COUNT(*) as requests
               FROM usage_logs ul 
               JOIN api_keys ak ON ul.api_key_id = ak.id 
               WHERE ak.user_id = %s AND ul.timestamp >= NOW() - INTERVAL '24 hours'
               GROUP BY EXTRACT(HOUR FROM ul.timestamp)
               ORDER BY hour""",
            (user_id,),
            fetch=True
        )
        
        return {
            'total_requests': total_requests,
            'this_month_requests': this_month_requests,
            'api_key_count': api_key_count,
            'chart_data': [{'hour': int(d['hour']), 'requests': d['requests']} for d in chart_data]
        }
    
    @staticmethod
    def delete_api_key(user_id, api_key_id):
        """Delete an API key"""
        execute_query(
            "UPDATE api_keys SET is_active = FALSE WHERE id = %s AND user_id = %s",
            (api_key_id, user_id)
        )
    
    @staticmethod
    def delete_user_account(user_id):
        """Permanently delete user account and all data"""
        execute_query("DELETE FROM users WHERE id = %s", (user_id,))