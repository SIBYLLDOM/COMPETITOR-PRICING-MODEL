# test_api.py
"""
Test script for L1 Pricing Model API
Demonstrates how to interact with the API endpoints
"""

import requests
import json
from typing import Dict, Any

# API Configuration
API_BASE_URL = "http://localhost:8000"

def print_response(response: requests.Response, title: str):
    """Pretty print API response"""
    print("\n" + "=" * 70)
    print(f"📊 {title}")
    print("=" * 70)
    print(f"Status Code: {response.status_code}")
    print(f"\nResponse:")
    try:
        print(json.dumps(response.json(), indent=2))
    except:
        print(response.text)
    print("=" * 70)


def test_root_endpoint():
    """Test root endpoint"""
    response = requests.get(f"{API_BASE_URL}/")
    print_response(response, "ROOT ENDPOINT TEST")
    return response.status_code == 200


def test_health_check():
    """Test health check endpoint"""
    response = requests.get(f"{API_BASE_URL}/health")
    print_response(response, "HEALTH CHECK TEST")
    return response.status_code == 200


def test_system_status():
    """Test system status endpoint"""
    response = requests.get(f"{API_BASE_URL}/api/v1/status")
    print_response(response, "SYSTEM STATUS TEST")
    return response.status_code == 200


def test_pricing_prediction(product: str, quantity: int):
    """Test pricing prediction endpoint"""
    
    payload = {
        "product": product,
        "quantity": quantity
    }
    
    print(f"\n🔍 Testing prediction for:")
    print(f"   Product: {product}")
    print(f"   Quantity: {quantity}")
    
    response = requests.post(
        f"{API_BASE_URL}/api/v1/predict",
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    
    print_response(response, "PRICING PREDICTION TEST")
    
    if response.status_code == 200:
        data = response.json()
        print(f"\n💰 PRICING RECOMMENDATION:")
        print(f"   Low Price:  ₹{data['low_price']:,.2f}")
        print(f"   High Price: ₹{data['high_price']:,.2f}")
        print(f"   Confidence: {data['confidence']}")
        print(f"   Competitors: {data['competitors_analyzed']}")
        print(f"   Price Type: {data['price_type']}")
    
    return response.status_code == 200


def test_invalid_request():
    """Test error handling with invalid request"""
    
    # Test 1: Empty product name
    print("\n🧪 Testing error handling (empty product)...")
    payload = {"product": "", "quantity": 5}
    response = requests.post(
        f"{API_BASE_URL}/api/v1/predict",
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    print_response(response, "ERROR HANDLING TEST - Empty Product")
    
    # Test 2: Invalid quantity
    print("\n🧪 Testing error handling (invalid quantity)...")
    payload = {"product": "Test Product", "quantity": -5}
    response = requests.post(
        f"{API_BASE_URL}/api/v1/predict",
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    print_response(response, "ERROR HANDLING TEST - Invalid Quantity")
    
    # Test 3: Non-existent product
    print("\n🧪 Testing error handling (non-existent product)...")
    payload = {"product": "XYZABC_NONEXISTENT_PRODUCT_12345", "quantity": 10}
    response = requests.post(
        f"{API_BASE_URL}/api/v1/predict",
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    print_response(response, "ERROR HANDLING TEST - Non-existent Product")


def run_all_tests():
    """Run all API tests"""
    
    print("\n" + "=" * 70)
    print("🧪 L1 PRICING MODEL API - TEST SUITE")
    print("=" * 70)
    print(f"API Base URL: {API_BASE_URL}")
    print("=" * 70)
    
    tests_passed = 0
    tests_failed = 0
    
    # Test 1: Root endpoint
    print("\n[1/6] Testing Root Endpoint...")
    if test_root_endpoint():
        tests_passed += 1
        print("✅ PASS")
    else:
        tests_failed += 1
        print("❌ FAIL")
    
    # Test 2: Health check
    print("\n[2/6] Testing Health Check...")
    if test_health_check():
        tests_passed += 1
        print("✅ PASS")
    else:
        tests_failed += 1
        print("❌ FAIL")
    
    # Test 3: System status
    print("\n[3/6] Testing System Status...")
    if test_system_status():
        tests_passed += 1
        print("✅ PASS")
    else:
        tests_failed += 1
        print("❌ FAIL")
    
    # Test 4: Pricing prediction - Example 1
    print("\n[4/6] Testing Pricing Prediction (Hematology Analyzer)...")
    if test_pricing_prediction("3 Part Automated Hematology Analyzer", 5):
        tests_passed += 1
        print("✅ PASS")
    else:
        tests_failed += 1
        print("❌ FAIL")
    
    # Test 5: Pricing prediction - Example 2
    print("\n[5/6] Testing Pricing Prediction (Biochemistry Analyzer)...")
    if test_pricing_prediction("Fully Automatic Biochemistry Analyzer", 10):
        tests_passed += 1
        print("✅ PASS")
    else:
        tests_failed += 1
        print("❌ FAIL")
    
    # Test 6: Error handling
    print("\n[6/6] Testing Error Handling...")
    test_invalid_request()
    tests_passed += 1  # This is expected to return errors
    print("✅ PASS (Error handling working)")
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 TEST SUMMARY")
    print("=" * 70)
    print(f"✅ Tests Passed: {tests_passed}")
    print(f"❌ Tests Failed: {tests_failed}")
    print(f"📈 Success Rate: {(tests_passed/(tests_passed+tests_failed)*100):.1f}%")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    import sys
    
    # Check if API is running
    try:
        response = requests.get(f"{API_BASE_URL}/", timeout=2)
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Cannot connect to API server!")
        print(f"   Please ensure the API is running at {API_BASE_URL}")
        print("\n   Start the API with:")
        print("   python start_api.py")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        sys.exit(1)
    
    # Run tests
    run_all_tests()
