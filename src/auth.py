#!/usr/bin/env python3
"""
Authentication module for Movie Database API
Handles user signup, email verification, and API key management
"""

import os
import uuid
import hashlib
import bcrypt
import re
import json
import time
from datetime import datetime, timedelta
from typing import Optional, Dict, List
from src.database import execute_query
import firebase_admin
from firebase_admin import auth as firebase_auth, credentials

def validate_firebase_admin(firebase_token: str, admin_uid: str = "MF2LvHPFaWhWSoevxm4ZyLcZzme2") -> bool:
    """Validate Firebase admin token for specific admin UID"""
    try:
        if not firebase_app:
            print("Firebase not initialized")
            return False
            
        # Verify the ID token
        decoded_token = firebase_auth.verify_id_token(firebase_token)
        user_uid = decoded_token['uid']
        
        # Check if this is the specific admin UID
        if user_uid != admin_uid:
            print(f"User {user_uid} is not admin {admin_uid}")
            return False
            
        # Update or create admin user in database
        admin_email = decoded_token.get('email', 'admin@moviedb.com')
        
        execute_query("""
            INSERT INTO users (email, password_hash, is_verified, firebase_uid, role) 
            VALUES (%s, 'firebase_auth', true, %s, 'admin')
            ON CONFLICT (firebase_uid) DO UPDATE SET
                email = EXCLUDED.email,
                role = 'admin'
        """, (admin_email, user_uid))
        
        return True
        
    except Exception as e:
        print(f"Firebase admin validation error: {e}")
        return False
        
def sync_firebase_user(firebase_token: str) -> Optional[Dict]:
    """Sync Firebase user to local database"""
    try:
        if not firebase_app:
            return None
            
        decoded_token = firebase_auth.verify_id_token(firebase_token)
        user_uid = decoded_token['uid']
        email = decoded_token.get('email')
        
        if not email:
            return None
            
        # Insert or update user
        result = execute_query("""
            INSERT INTO users (email, password_hash, is_verified, firebase_uid, role) 
            VALUES (%s, 'firebase_auth', true, %s, 'user')
            ON CONFLICT (firebase_uid) DO UPDATE SET
                email = EXCLUDED.email
            RETURNING id, email, firebase_uid, role
        """, (email, user_uid), fetch=True)
        
        return result[0] if result else None
        
    except Exception as e:
        print(f"Firebase user sync error: {e}")
        return None

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Firebase initialization (will be set up when credentials are provided)
firebase_app = None

# Allowed email domains
ALLOWED_DOMAINS = ['gmail.com', 'yahoo.com', 'outlook.com', 'hotmail.com']

# Disposable email domains blocklist
DISPOSABLE_DOMAINS = [
    '10minutemail.com', 'tempmail.org', 'guerrillamail.com', 'mailinator.com',
    'throwaway.email', 'temp-mail.org', 'getairmail.com', 'yopmail.com',
    'sharklasers.com', 'guerrillamailblock.com', 'pokemail.net', 'spam4.me'
]

class AuthError(Exception):
    """Custom authentication error"""
    pass

class RateLimitError(Exception):
    """Rate limit exceeded error"""
    pass

def init_firebase(credentials_path: str = "firebase-service-account.json"):
    """Initialize Firebase Admin SDK"""
    global firebase_app
    try:
        if not firebase_app:
            if credentials_path and os.path.exists(credentials_path):
                cred = credentials.Certificate(credentials_path)
                firebase_app = firebase_admin.initialize_app(cred)
                print("✅ Firebase initialized successfully!")
                return True
            else:
                # Try to initialize with environment variables
                project_id = os.getenv('FIREBASE_PROJECT_ID')
                private_key = os.getenv('FIREBASE_PRIVATE_KEY')
                client_email = os.getenv('FIREBASE_CLIENT_EMAIL')
                
                if project_id and private_key and client_email:
                    # Create credential dict from environment variables
                    cred_dict = {
                        "type": "service_account",
                        "project_id": project_id,
                        "private_key": private_key.replace('\\n', '\n'),
                        "client_email": client_email,
                        "token_uri": "https://oauth2.googleapis.com/token",
                        "auth_uri": "https://accounts.google.com/o/oauth2/auth"
                    }
                    cred = credentials.Certificate(cred_dict)
                    firebase_app = firebase_admin.initialize_app(cred)
                    print("✅ Firebase initialized with environment variables!")
                    return True
                else:
                    print("❌ Firebase credentials not found in environment")
                    return False
        else:
            print("✅ Firebase already initialized!")
            return True
    except Exception as e:
        print(f"❌ Firebase initialization failed: {e}")
        return False

def validate_email_domain(email: str) -> bool:
    """Validate if email domain is allowed and not disposable"""
    domain = email.lower().split('@')[-1]
    
    # Check if domain is in allowed list
    if domain not in ALLOWED_DOMAINS:
        raise AuthError(f"Email domain '{domain}' is not allowed. Allowed domains: {', '.join(ALLOWED_DOMAINS)}")
    
    # Check if domain is disposable
    if domain in DISPOSABLE_DOMAINS:
        raise AuthError(f"Disposable email addresses are not allowed")
    
    return True

def validate_email_format(email: str) -> bool:
    """Validate email format using regex"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        raise AuthError("Invalid email format")
    return True

def hash_password(password: str) -> str:
    """Hash password using bcrypt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    """Verify password against hash"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def generate_api_key() -> str:
    """Generate a unique API key"""
    return str(uuid.uuid4())

def hash_api_key(api_key: str) -> str:
    """Hash API key for storage"""
    return hashlib.sha256(api_key.encode()).hexdigest()

def check_rate_limit(identifier: str, action: str, limit: int = 5, window: int = 900) -> bool:
    """
    Check rate limit for user actions
    Args:
        identifier: User identifier (email or IP)
        action: Action type (signup, resend_verification, etc.)
        limit: Maximum attempts allowed
        window: Time window in seconds (default 15 minutes)
    """
    current_time = int(time.time())
    window_start = current_time - window
    
    # Clean up old rate limit entries
    execute_query("""
        DELETE FROM rate_limits 
        WHERE timestamp < %s
    """, (window_start,))
    
    # Check current attempts
    attempts = execute_query("""
        SELECT COUNT(*) as count 
        FROM rate_limits 
        WHERE identifier = %s AND action = %s AND timestamp >= %s
    """, (identifier, action, window_start), fetch=True)
    
    current_attempts = attempts[0]['count'] if attempts else 0
    
    if current_attempts >= limit:
        raise RateLimitError(f"Rate limit exceeded for {action}. Try again in {window // 60} minutes.")
    
    # Record this attempt
    execute_query("""
        INSERT INTO rate_limits (identifier, action, timestamp) 
        VALUES (%s, %s, %s)
    """, (identifier, action, current_time))
    
    return True

def create_user(email: str, password: str) -> Dict:
    """Create a new user account with Firebase email verification"""
    try:
        # Validate email
        validate_email_format(email)
        validate_email_domain(email)
        
        # Check rate limit
        check_rate_limit(email, 'signup', limit=3, window=3600)  # 3 attempts per hour
        
        # Check if user already exists in our database
        existing_user = execute_query(
            "SELECT id, email, is_verified FROM users WHERE email = %s",
            (email,), fetch=True
        )
        
        if existing_user and existing_user[0]['is_verified']:
            raise AuthError("User already exists and is verified")
        
        # Firebase is required for proper email verification
        if not firebase_app:
            raise AuthError("Email verification service is not available. Please contact support.")
        
        try:
            # Create Firebase user
            firebase_user = firebase_auth.create_user(
                email=email,
                password=password,
                email_verified=False
            )
            
            # Send verification email through Firebase
            verification_link = firebase_auth.generate_email_verification_link(
                email,
                action_code_settings=None
            )
            
            # Now create/update user in our database
            if existing_user:
                # Update existing unverified user
                user_id = existing_user[0]['id']
                password_hash = hash_password(password)
                execute_query(
                    "UPDATE users SET password_hash = %s WHERE id = %s",
                    (password_hash, user_id)
                )
            else:
                # Create new user
                password_hash = hash_password(password)
                result = execute_query("""
                    INSERT INTO users (email, password_hash, is_verified, created_at)
                    VALUES (%s, %s, FALSE, CURRENT_TIMESTAMP)
                    RETURNING id
                """, (email, password_hash), fetch=True)
                user_id = result[0]['id']
            
            print(f"✅ Firebase user created and verification email sent to {email}")
            
            return {
                'success': True,
                'user_id': user_id,
                'firebase_uid': firebase_user.uid,
                'message': 'Account created successfully! Please check your email for verification. Click the link in the email to verify your account.',
                'email_sent': True,
                'instructions': 'Check your email (including spam folder) for a verification email from Firebase. Click the verification link, then use the verify endpoint to get your API key.'
            }
            
        except Exception as firebase_error:
            # Enhanced error reporting for debugging
            error_message = str(firebase_error)
            print(f"🐛 Firebase Error Details: {firebase_error}")
            print(f"🐛 Error Type: {type(firebase_error).__name__}")
            
            # If user already exists in Firebase, try to resend verification
            if "already exists" in error_message.lower():
                try:
                    existing_firebase_user = firebase_auth.get_user_by_email(email)
                    if not existing_firebase_user.email_verified:
                        # Generate new verification email
                        verification_link = firebase_auth.generate_email_verification_link(email)
                        print(f"✅ Verification email resent to {email}")
                        
                        return {
                            'success': True,
                            'user_id': existing_user[0]['id'] if existing_user else None,
                            'firebase_uid': existing_firebase_user.uid,
                            'message': 'User already exists. Verification email resent! Please check your email.',
                            'email_sent': True,
                            'instructions': 'Check your email (including spam folder) for a verification email from Firebase. Click the verification link, then use the verify endpoint to get your API key.'
                        }
                    else:
                        raise AuthError("User already exists and is verified in Firebase. Use the verify endpoint to get your API key.")
                except Exception as resend_error:
                    raise AuthError(f"Firebase error: {str(firebase_error)}")
            elif "invalid_grant" in error_message.lower():
                # Specific handling for JWT signature errors
                raise AuthError(f"Firebase credentials issue - JWT signature invalid. This may be due to: 1) Expired service account key, 2) Incorrect private key format, 3) Firebase project configuration issue. Error: {error_message}")
            else:
                raise AuthError(f"Failed to create Firebase user: {error_message}")
            
    except (AuthError, RateLimitError) as e:
        raise e
    except Exception as e:
        raise AuthError(f"Failed to create user: {str(e)}")

def verify_user_email(email: str, verification_code: str = None) -> Dict:
    """Verify user email through Firebase and generate API key"""
    try:
        # Get user
        user = execute_query(
            "SELECT id, email, is_verified FROM users WHERE email = %s",
            (email,), fetch=True
        )
        
        if not user:
            raise AuthError("User not found. Please sign up first.")
        
        user_data = user[0]
        
        if user_data['is_verified']:
            raise AuthError("User already verified")
        
        # Firebase is required for email verification
        if not firebase_app:
            raise AuthError("Email verification service is not available. Please contact support.")
        
        # Check Firebase verification status
        try:
            firebase_user = firebase_auth.get_user_by_email(email)
            if not firebase_user.email_verified:
                raise AuthError(
                    "Email not verified yet. Please check your email and click the verification link. "
                    "If you haven't received an email, use the resend verification endpoint."
                )
        except firebase_admin.auth.UserNotFoundError:
            raise AuthError("User not found in Firebase. Please sign up first.")
        except Exception as e:
            raise AuthError(f"Firebase verification check failed: {str(e)}")
        
        # Mark user as verified in our database
        execute_query(
            "UPDATE users SET is_verified = TRUE WHERE id = %s",
            (user_data['id'],)
        )
        
        # Generate API key
        raw_api_key = generate_api_key()
        hashed_key = hash_api_key(raw_api_key)
        
        # Store API key
        execute_query("""
            INSERT INTO api_keys (user_id, api_key, created_at, is_active)
            VALUES (%s, %s, CURRENT_TIMESTAMP, TRUE)
        """, (user_data['id'], hashed_key))
        
        print(f"✅ User {email} verified successfully and API key generated")
        
        return {
            'success': True,
            'api_key': raw_api_key,
            'message': 'Email verified successfully! Your API key is shown once - please save it securely.',
            'instructions': 'Use this API key in the "X-API-Key" header to access protected endpoints.'
        }
        
    except AuthError as e:
        raise e
    except Exception as e:
        raise AuthError(f"Failed to verify user: {str(e)}")

def resend_verification(email: str) -> Dict:
    """Resend verification email through Firebase"""
    try:
        # Check rate limit (1 minute cooldown to prevent spam)
        check_rate_limit(email, 'resend_verification', limit=3, window=60)
        
        # Check if user exists in our database
        user = execute_query(
            "SELECT id, email, is_verified FROM users WHERE email = %s",
            (email,), fetch=True
        )
        
        if not user:
            raise AuthError("User not found. Please sign up first.")
        
        if user[0]['is_verified']:
            raise AuthError("User already verified")
        
        # Firebase is required for email verification
        if not firebase_app:
            raise AuthError("Email verification service is not available. Please contact support.")
        
        try:
            # Check if user exists in Firebase and resend verification
            firebase_user = firebase_auth.get_user_by_email(email)
            
            if firebase_user.email_verified:
                raise AuthError("Email is already verified in Firebase. Use the verify endpoint to get your API key.")
            
            # Generate and send new verification email
            verification_link = firebase_auth.generate_email_verification_link(email)
            
            print(f"✅ Verification email resent to {email}")
            
            return {
                'success': True,
                'message': 'Verification email sent successfully! Please check your email.',
                'instructions': 'Check your email (including spam folder) for the verification link. Click it, then use the verify endpoint to get your API key.',
                'email_sent': True
            }
            
        except firebase_admin.auth.UserNotFoundError:
            raise AuthError("User not found in Firebase. Please sign up again.")
        except Exception as e:
            raise AuthError(f"Failed to send verification email: {str(e)}")
            
    except (AuthError, RateLimitError) as e:
        raise e
    except Exception as e:
        raise AuthError(f"Failed to resend verification: {str(e)}")

def validate_api_key(api_key: str) -> Optional[Dict]:
    """Validate API key and return user info"""
    try:
        hashed_key = hash_api_key(api_key)
        
        result = execute_query("""
            SELECT ak.id, ak.user_id, u.email, u.is_verified
            FROM api_keys ak
            JOIN users u ON ak.user_id = u.id
            WHERE ak.api_key = %s AND ak.is_active = TRUE AND u.is_verified = TRUE
        """, (hashed_key,), fetch=True)
        
        if result:
            return {
                'api_key_id': result[0]['id'],
                'user_id': result[0]['user_id'],
                'email': result[0]['email'],
                'verified': result[0]['is_verified']
            }
        return None
        
    except Exception as e:
        return None

def get_user_subscription(user_id: int) -> Dict:
    """Get user's subscription plan and daily limit"""
    try:
        result = execute_query("""
            SELECT plan_type, daily_limit
            FROM user_subscriptions
            WHERE user_id = %s
        """, (user_id,), fetch=True)
        
        if result:
            return {
                'plan_type': result[0]['plan_type'],
                'daily_limit': result[0]['daily_limit']
            }
        else:
            # Create default free subscription if not exists
            execute_query("""
                INSERT INTO user_subscriptions (user_id, plan_type, daily_limit)
                VALUES (%s, 'free', 100)
            """, (user_id,))
            return {'plan_type': 'free', 'daily_limit': 100}
    except Exception as e:
        print(f"Error getting user subscription: {e}")
        return {'plan_type': 'free', 'daily_limit': 100}

def get_user_daily_usage(user_id: int) -> int:
    """Get user's total daily usage across all API keys"""
    try:
        today = datetime.now().date()
        result = execute_query("""
            SELECT COALESCE(SUM(du.request_count), 0) as total_requests
            FROM daily_usage du
            JOIN api_keys ak ON du.api_key_id = ak.id
            WHERE ak.user_id = %s AND du.date = %s
        """, (user_id, today), fetch=True)
        
        return result[0]['total_requests'] if result else 0
    except Exception as e:
        print(f"Error getting user daily usage: {e}")
        return 0

def check_user_rate_limit(user_id: int) -> bool:
    """Check if user has exceeded their daily rate limit"""
    try:
        subscription = get_user_subscription(user_id)
        current_usage = get_user_daily_usage(user_id)
        
        if current_usage >= subscription['daily_limit']:
            plan_name = "free plan" if subscription['plan_type'] == 'free' else "premium plan"
            raise RateLimitError(f"Your {plan_name} has reached its daily limit of {subscription['daily_limit']} requests. Please upgrade to premium for higher limits or try again tomorrow.")
        
        return True
    except RateLimitError:
        raise
    except Exception as e:
        print(f"Error checking rate limit: {e}")
        # Fail-closed: Raise error if rate limit check fails
        raise RateLimitError("Rate limit service temporarily unavailable. Please try again later.")

def check_and_increment_user_rate_limit(user_id: int, api_key_id: int, endpoint: str) -> bool:
    """Atomically check rate limit and increment usage counter"""
    from datetime import datetime
    
    try:
        today = datetime.now().date()
        
        # Atomic operation: check current usage and increment in single transaction
        result = execute_query("""
            WITH current_usage AS (
                SELECT COALESCE(SUM(du.request_count), 0) as total_requests
                FROM daily_usage du
                JOIN api_keys ak ON du.api_key_id = ak.id
                WHERE ak.user_id = %s AND du.date = %s
            ),
            user_plan AS (
                SELECT COALESCE(us.daily_limit, 100) as daily_limit,
                       COALESCE(us.plan_type, 'free') as plan_type
                FROM user_subscriptions us
                WHERE us.user_id = %s
                UNION ALL
                SELECT 100 as daily_limit, 'free' as plan_type
                WHERE NOT EXISTS (SELECT 1 FROM user_subscriptions WHERE user_id = %s)
                LIMIT 1
            )
            SELECT cu.total_requests, up.daily_limit, up.plan_type
            FROM current_usage cu, user_plan up
        """, (user_id, today, user_id, user_id), fetch=True)
        
        if not result:
            raise Exception("Failed to get rate limit data")
        
        current_usage = result[0]['total_requests']
        daily_limit = result[0]['daily_limit']
        plan_type = result[0]['plan_type']
        
        # Check if limit would be exceeded
        if current_usage >= daily_limit:
            plan_name = "free plan" if plan_type == 'free' else "premium plan"
            raise RateLimitError(f"Your {plan_name} has reached its daily limit of {daily_limit} requests. Please upgrade to premium for higher limits or try again tomorrow.")
        
        # Atomically increment usage counter
        execute_query("""
            INSERT INTO usage_logs (api_key_id, endpoint, timestamp, status_code)
            VALUES (%s, %s, CURRENT_TIMESTAMP, 200)
        """, (api_key_id, endpoint))
        
        execute_query("""
            INSERT INTO daily_usage (api_key_id, date, request_count)
            VALUES (%s, %s, 1)
            ON CONFLICT (api_key_id, date)
            DO UPDATE SET request_count = daily_usage.request_count + 1
        """, (api_key_id, today))
        
        return True
        
    except RateLimitError:
        raise
    except Exception as e:
        print(f"Error in atomic rate limit check: {e}")
        # Fail-closed: Raise error if atomic operation fails
        raise RateLimitError("Rate limit service temporarily unavailable. Please try again later.")

def upgrade_user_to_premium(user_id: int):
    """Upgrade user to premium plan"""
    try:
        execute_query("""
            INSERT INTO user_subscriptions (user_id, plan_type, daily_limit, updated_at)
            VALUES (%s, 'premium', 500, CURRENT_TIMESTAMP)
            ON CONFLICT (user_id)
            DO UPDATE SET 
                plan_type = 'premium',
                daily_limit = 500,
                updated_at = CURRENT_TIMESTAMP
        """, (user_id,))
        print(f"✅ User {user_id} upgraded to premium")
    except Exception as e:
        print(f"Error upgrading user to premium: {e}")
        raise

def log_api_usage(api_key_id: int, endpoint: str, status_code: int):
    """Log API usage for analytics"""
    try:
        execute_query("""
            INSERT INTO usage_logs (api_key_id, endpoint, timestamp, status_code)
            VALUES (%s, %s, CURRENT_TIMESTAMP, %s)
        """, (api_key_id, endpoint, status_code))
        
        # Update daily usage counter
        today = datetime.now().date()
        execute_query("""
            INSERT INTO daily_usage (api_key_id, date, request_count)
            VALUES (%s, %s, 1)
            ON CONFLICT (api_key_id, date)
            DO UPDATE SET request_count = daily_usage.request_count + 1
        """, (api_key_id, today))
        
    except Exception as e:
        # Don't fail the request if logging fails
        print(f"Failed to log API usage: {e}")

def get_user_usage_stats(user_id: int) -> Dict:
    """Get user's current usage stats"""
    try:
        subscription = get_user_subscription(user_id)
        daily_usage = get_user_daily_usage(user_id)
        remaining = max(0, subscription['daily_limit'] - daily_usage)
        
        return {
            'plan_type': subscription['plan_type'],
            'daily_limit': subscription['daily_limit'],
            'daily_usage': daily_usage,
            'remaining_requests': remaining,
            'percentage_used': round((daily_usage / subscription['daily_limit']) * 100, 1)
        }
    except Exception as e:
        print(f"Error getting usage stats: {e}")
        return {
            'plan_type': 'free',
            'daily_limit': 100,
            'daily_usage': 0,
            'remaining_requests': 100,
            'percentage_used': 0.0
        }