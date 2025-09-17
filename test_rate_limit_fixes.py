#!/usr/bin/env python3
"""
Test the rate limiting security fixes
"""
import requests
import time
import json

API_BASE = "http://localhost:5000"

def test_endpoints():
    """Test the basic endpoints to ensure they're working"""
    try:
        # Test root endpoint
        response = requests.get(f"{API_BASE}/")
        if response.status_code == 200:
            print("✅ API is running")
            return True
        else:
            print(f"❌ API not responding: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Cannot connect to API: {e}")
        return False

def create_test_user():
    """Create a test user and return API key"""
    try:
        signup_data = {
            "email": f"ratetest{int(time.time())}@gmail.com",
            "password": "testpass123"
        }
        
        response = requests.post(f"{API_BASE}/auth/register", json=signup_data)
        print(f"Registration response: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            api_key = data.get('api_key')
            if api_key:
                print(f"✅ Created test user with API key: {api_key[:10]}...")
                return api_key
            else:
                print("❌ No API key in registration response")
                print(f"Response: {data}")
                return None
        else:
            print(f"❌ Registration failed: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Registration error: {e}")
        return None

def test_management_endpoints_exemption(api_key):
    """Test that management endpoints are exempt from rate limiting"""
    print("\n🧪 Testing management endpoints exemption...")
    
    headers = {'X-API-Key': api_key}
    
    # Test quota endpoint multiple times - should not be rate limited
    quota_responses = []
    for i in range(3):
        response = requests.get(f"{API_BASE}/api/user/quota", headers=headers)
        quota_responses.append((response.status_code, response.json() if response.status_code == 200 else response.text))
        print(f"   Quota request {i+1}: {response.status_code}")
    
    # All quota requests should succeed
    success_count = sum(1 for status, _ in quota_responses if status == 200)
    if success_count == 3:
        print("✅ Management endpoints exempt from rate limiting")
        return True
    else:
        print(f"❌ Management endpoints not exempt: {success_count}/3 succeeded")
        return False

def test_normal_endpoint_rate_limiting(api_key):
    """Test that normal endpoints are subject to rate limiting"""
    print("\n🧪 Testing normal endpoint rate limiting...")
    
    headers = {'X-API-Key': api_key}
    
    # Test movies endpoint - should increment usage
    movie_responses = []
    for i in range(3):
        response = requests.get(f"{API_BASE}/api/movies", headers=headers)
        movie_responses.append((response.status_code, response.json() if response.status_code == 200 else response.text))
        print(f"   Movies request {i+1}: {response.status_code}")
        
        # Check quota after each request
        quota_response = requests.get(f"{API_BASE}/api/user/quota", headers=headers)
        if quota_response.status_code == 200:
            quota_data = quota_response.json()
            print(f"     Usage: {quota_data.get('daily_usage', 0)}/{quota_data.get('daily_limit', 100)}")
    
    # Check if usage increased
    quota_response = requests.get(f"{API_BASE}/api/user/quota", headers=headers)
    if quota_response.status_code == 200:
        final_usage = quota_response.json().get('daily_usage', 0)
        if final_usage >= 3:
            print("✅ Normal endpoints increment usage correctly")
            return True
        else:
            print(f"❌ Usage not incremented correctly: {final_usage}")
            return False
    else:
        print("❌ Cannot check final usage")
        return False

def test_fail_closed_behavior():
    """Test fail-closed behavior with invalid API key"""
    print("\n🧪 Testing fail-closed behavior...")
    
    headers = {'X-API-Key': 'invalid-key-12345'}
    
    response = requests.get(f"{API_BASE}/api/movies", headers=headers)
    
    if response.status_code == 401:
        print("✅ Invalid API key properly rejected")
        return True
    else:
        print(f"❌ Invalid API key not rejected: {response.status_code}")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing Rate Limiting Security Fixes")
    print("=" * 50)
    
    # Check if API is running
    if not test_endpoints():
        return
    
    # Create test user
    api_key = create_test_user()
    if not api_key:
        print("❌ Cannot create test user - skipping rate limiting tests")
        return
    
    # Test the fixes
    results = []
    results.append(test_management_endpoints_exemption(api_key))
    results.append(test_normal_endpoint_rate_limiting(api_key))
    results.append(test_fail_closed_behavior())
    
    # Summary
    print("\n📊 Test Results:")
    print("=" * 30)
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print(f"✅ All tests passed ({passed}/{total})")
        print("✅ Rate limiting security fixes are working correctly")
    else:
        print(f"❌ Some tests failed ({passed}/{total})")
        print("❌ Rate limiting security fixes need review")

if __name__ == "__main__":
    main()