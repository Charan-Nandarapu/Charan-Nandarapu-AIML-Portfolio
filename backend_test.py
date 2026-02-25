#!/usr/bin/env python3
"""
Backend API Tests for Charan's Portfolio Contact Form
Tests the contact form API endpoints for proper functionality
"""

import requests
import json
import sys
from datetime import datetime
import uuid

# Test configuration
BASE_URL = "https://portfolio-pro-322.preview.emergentagent.com/api"
CONTACT_ENDPOINT = f"{BASE_URL}/contact"

def log_test_result(test_name, success, details=""):
    """Log test results with consistent formatting"""
    status = "✅ PASS" if success else "❌ FAIL"
    print(f"\n{status} {test_name}")
    if details:
        print(f"   Details: {details}")

def test_successful_contact_submission():
    """Test successful contact message submission"""
    print("\n" + "="*60)
    print("TEST 1: Successful Contact Message Submission")
    print("="*60)
    
    test_data = {
        "name": "John Doe",
        "email": "john@example.com",
        "subject": "Job Opportunity",
        "message": "Hi Charan, I'd like to discuss a position at our company."
    }
    
    try:
        response = requests.post(CONTACT_ENDPOINT, json=test_data, timeout=30)
        print(f"Response Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        
        if response.status_code == 201:
            data = response.json()
            print(f"Response Data: {json.dumps(data, indent=2)}")
            
            # Validate response structure
            if (data.get("success") is True and 
                "message" in data and 
                "data" in data and 
                data["data"].get("id") and
                data["data"].get("timestamp") and
                data["data"].get("status") == "unread"):
                
                log_test_result("Contact message submission", True, 
                               f"Message ID: {data['data']['id']}")
                return data["data"]["id"]  # Return ID for later tests
            else:
                log_test_result("Contact message submission", False, 
                               "Response structure validation failed")
                return None
        else:
            log_test_result("Contact message submission", False, 
                           f"Expected 201, got {response.status_code}: {response.text}")
            return None
            
    except requests.exceptions.RequestException as e:
        log_test_result("Contact message submission", False, f"Request failed: {str(e)}")
        return None

def test_invalid_email_format():
    """Test invalid email format validation"""
    print("\n" + "="*60)
    print("TEST 2: Invalid Email Format Validation")
    print("="*60)
    
    test_data = {
        "name": "Jane Doe",
        "email": "invalid-email",
        "subject": "Test",
        "message": "This should fail"
    }
    
    try:
        response = requests.post(CONTACT_ENDPOINT, json=test_data, timeout=30)
        print(f"Response Status Code: {response.status_code}")
        
        if response.status_code == 422:
            data = response.json()
            print(f"Validation Error Response: {json.dumps(data, indent=2)}")
            log_test_result("Invalid email validation", True, 
                           "422 validation error returned as expected")
        else:
            log_test_result("Invalid email validation", False, 
                           f"Expected 422, got {response.status_code}: {response.text}")
            
    except requests.exceptions.RequestException as e:
        log_test_result("Invalid email validation", False, f"Request failed: {str(e)}")

def test_missing_required_fields():
    """Test missing required fields validation"""
    print("\n" + "="*60)
    print("TEST 3: Missing Required Fields Validation")
    print("="*60)
    
    test_data = {
        "name": "Test User"
        # Missing email, subject, message
    }
    
    try:
        response = requests.post(CONTACT_ENDPOINT, json=test_data, timeout=30)
        print(f"Response Status Code: {response.status_code}")
        
        if response.status_code == 422:
            data = response.json()
            print(f"Validation Error Response: {json.dumps(data, indent=2)}")
            log_test_result("Missing fields validation", True, 
                           "422 validation error returned as expected")
        else:
            log_test_result("Missing fields validation", False, 
                           f"Expected 422, got {response.status_code}: {response.text}")
            
    except requests.exceptions.RequestException as e:
        log_test_result("Missing fields validation", False, f"Request failed: {str(e)}")

def test_get_all_messages():
    """Test GET all contact messages"""
    print("\n" + "="*60)
    print("TEST 4: GET All Contact Messages")
    print("="*60)
    
    try:
        response = requests.get(CONTACT_ENDPOINT, timeout=30)
        print(f"Response Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Response Data: {json.dumps(data, indent=2)}")
            
            # Validate response structure
            if (data.get("success") is True and 
                "count" in data and 
                "data" in data and 
                isinstance(data["data"], list)):
                
                message_count = data.get("count", 0)
                log_test_result("GET all messages", True, 
                               f"Retrieved {message_count} messages")
                
                # Check if our test message is present
                test_message_found = any(
                    msg.get("email") == "john@example.com" 
                    for msg in data["data"]
                )
                
                if test_message_found:
                    print("   ✅ Test message from previous submission found")
                else:
                    print("   ⚠️  Test message from previous submission not found")
                    
                return True
            else:
                log_test_result("GET all messages", False, 
                               "Response structure validation failed")
                return False
        else:
            log_test_result("GET all messages", False, 
                           f"Expected 200, got {response.status_code}: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        log_test_result("GET all messages", False, f"Request failed: {str(e)}")
        return False

def test_empty_message_fields():
    """Test empty message fields validation"""
    print("\n" + "="*60)
    print("TEST 5: Empty Message Fields Validation")
    print("="*60)
    
    test_cases = [
        {
            "name": "",
            "email": "test@example.com",
            "subject": "Test",
            "message": "Valid message"
        },
        {
            "name": "Test User",
            "email": "test@example.com",
            "subject": "",
            "message": "Valid message"
        },
        {
            "name": "Test User",
            "email": "test@example.com",
            "subject": "Test",
            "message": ""
        }
    ]
    
    all_passed = True
    
    for i, test_data in enumerate(test_cases, 1):
        try:
            response = requests.post(CONTACT_ENDPOINT, json=test_data, timeout=30)
            print(f"Test Case {i} - Response Status Code: {response.status_code}")
            
            if response.status_code == 422:
                print(f"   ✅ Empty field validation working for case {i}")
            else:
                print(f"   ❌ Expected 422 for case {i}, got {response.status_code}")
                all_passed = False
                
        except requests.exceptions.RequestException as e:
            print(f"   ❌ Request failed for case {i}: {str(e)}")
            all_passed = False
    
    log_test_result("Empty fields validation", all_passed, 
                   "All empty field cases handled properly" if all_passed else "Some cases failed")

def test_backend_health():
    """Test if backend service is running"""
    print("\n" + "="*60)
    print("PRELIMINARY: Backend Health Check")
    print("="*60)
    
    health_url = f"{BASE_URL}/"
    
    try:
        response = requests.get(health_url, timeout=10)
        print(f"Health Check Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Health Check Response: {json.dumps(data, indent=2)}")
            log_test_result("Backend health check", True, "Backend is responsive")
            return True
        else:
            log_test_result("Backend health check", False, 
                           f"Unexpected status code: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        log_test_result("Backend health check", False, f"Backend unreachable: {str(e)}")
        return False

def run_all_tests():
    """Run all contact form API tests"""
    print("🚀 Starting Contact Form API Tests")
    print("Backend URL:", BASE_URL)
    print("Contact Endpoint:", CONTACT_ENDPOINT)
    
    # Check backend health first
    if not test_backend_health():
        print("\n❌ CRITICAL: Backend is not accessible. Aborting tests.")
        return False
    
    # Run all tests
    test_results = []
    
    # Test 1: Successful submission
    message_id = test_successful_contact_submission()
    test_results.append(message_id is not None)
    
    # Test 2: Invalid email
    test_invalid_email_format()
    
    # Test 3: Missing fields
    test_missing_required_fields()
    
    # Test 4: GET all messages
    get_success = test_get_all_messages()
    test_results.append(get_success)
    
    # Test 5: Empty fields
    test_empty_message_fields()
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed_count = sum(1 for result in test_results if result)
    total_count = len(test_results)
    
    print(f"Core functionality tests: {passed_count}/{total_count} passed")
    
    if passed_count == total_count:
        print("✅ All critical tests passed - Contact API is working correctly!")
        return True
    else:
        print("❌ Some critical tests failed - Contact API has issues")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)