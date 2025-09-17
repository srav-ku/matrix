#!/usr/bin/env python3
"""
Test script for API rate limiting functionality
Tests both free plan (100 requests/day) and premium plan (500 requests/day)
"""

import requests
import json
import time
import sys

API_BASE_URL = "http://localhost:8000"

def create_test_user(email, password):
    """Create a test user and return their API key"""
    try:
        # Register user
        register_data = {
            'email': email,
            'password': password
        }
        
        response = requests.post(f"{API_BASE_URL}/auth/register", json=register_data)
        
        if response.status_code == 201:
            result = response.json()
            print(f"✅ User {email} created successfully")
            if 'api_key' in result:
                return result['api_key']
            return None
        else:
            # Check if user already exists and try to login
            if response.status_code == 400 and "already exists" in response.text:
                print(f"ℹ️  User {email} already exists, attempting login...")
                user_response = requests.post(f"{API_BASE_URL}/auth/login", json=register_data)
                if user_response.status_code == 200:
                    user_data = user_response.json()
                    if 'api_key' in user_data:
                        return user_data['api_key']
            
            print(f"❌ Failed to create user {email}: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error creating user {email}: {e}")
        return None

def test_api_endpoint(api_key, endpoint="/api/movies"):
    """Test API endpoint with given API key"""
    headers = {'X-API-Key': api_key}
    try:
        response = requests.get(f"{API_BASE_URL}{endpoint}", headers=headers)
        return response.status_code, response.json()
    except Exception as e:
        return 500, {'error': str(e)}

def get_user_quota(api_key):
    """Get user's current quota information"""
    headers = {'X-API-Key': api_key}
    try:
        response = requests.get(f"{API_BASE_URL}/api/user/quota", headers=headers)
        if response.status_code == 200:
            return response.json()
        return {'error': f"Status {response.status_code}: {response.text}"}
    except Exception as e:
        return {'error': str(e)}

def upgrade_user(api_key):
    """Upgrade user to premium"""
    headers = {'X-API-Key': api_key}
    try:
        response = requests.post(f"{API_BASE_URL}/api/user/upgrade", headers=headers)
        return response.status_code, response.json()
    except Exception as e:
        return 500, {'error': str(e)}

def test_rate_limiting():
    """Main test function"""
    print("🧪 Testing API Rate Limiting System")
    print("=" * 50)
    
    # Test data
    free_user_email = "test_free@gmail.com"
    premium_user_email = "test_premium@gmail.com"
    test_password = "testpassword123"
    
    # Create test users
    print("\n📝 Creating test users...")
    free_api_key = create_test_user(free_user_email, test_password)
    premium_api_key = create_test_user(premium_user_email, test_password)
    
    # For testing purposes, let's manually create API keys if user creation didn't return them
    if not free_api_key:
        print("⚠️  Free user API key not received, creating manually...")
        # We'll need to handle this case
        return
    
    if not premium_api_key:
        print("⚠️  Premium user API key not received, creating manually...")
        # We'll need to handle this case
        return
    
    print(f"✅ Free user API key: {free_api_key[:10]}...")
    print(f"✅ Premium user API key: {premium_api_key[:10]}...")
    
    # Test initial quotas
    print("\n📊 Checking initial quotas...")
    free_quota = get_user_quota(free_api_key)
    print(f"Free user quota: {free_quota}")
    
    premium_quota_initial = get_user_quota(premium_api_key)
    print(f"Premium user quota (before upgrade): {premium_quota_initial}")
    
    # Upgrade premium user
    print("\n⬆️  Upgrading premium user...")
    upgrade_status, upgrade_result = upgrade_user(premium_api_key)
    print(f"Upgrade result: {upgrade_result}")
    
    # Check premium quota after upgrade
    premium_quota = get_user_quota(premium_api_key)
    print(f"Premium user quota (after upgrade): {premium_quota}")
    
    # Test free user rate limiting (make 5 requests to test)
    print(f"\n🔄 Testing free user rate limiting (making 5 requests)...")
    free_requests = 0
    for i in range(5):
        status, result = test_api_endpoint(free_api_key)
        free_requests += 1
        if status == 429:
            print(f"❌ Request {i+1}: Rate limited - {result}")
            break
        elif status == 200:
            print(f"✅ Request {i+1}: Success - {len(result.get('movies', []))} movies returned")
        else:
            print(f"⚠️  Request {i+1}: Status {status} - {result}")
        
        # Check quota after each request
        quota = get_user_quota(free_api_key)
        print(f"   Current usage: {quota.get('daily_usage', 0)}/{quota.get('daily_limit', 100)}")
    
    # Test premium user (make 5 requests)
    print(f"\n🔄 Testing premium user rate limiting (making 5 requests)...")
    for i in range(5):
        status, result = test_api_endpoint(premium_api_key)
        if status == 429:
            print(f"❌ Request {i+1}: Rate limited - {result}")
            break
        elif status == 200:
            print(f"✅ Request {i+1}: Success - {len(result.get('movies', []))} movies returned")
        else:
            print(f"⚠️  Request {i+1}: Status {status} - {result}")
        
        # Check quota after each request
        quota = get_user_quota(premium_api_key)
        print(f"   Current usage: {quota.get('daily_usage', 0)}/{quota.get('daily_limit', 500)}")
    
    print("\n🏁 Rate limiting tests completed!")

if __name__ == "__main__":
    test_rate_limiting()