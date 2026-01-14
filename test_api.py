# test_api.py
"""
Test script for L1 Pricing Model API
"""
import requests
import json

# API endpoint
BASE_URL = "http://localhost:8000"

def test_health():
    """Test health check endpoint"""
    print("\n" + "=" * 70)
    print("🏥 TESTING HEALTH CHECK")
    print("=" * 70)
    
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status Code: {response.status_code}")
    print(f"Response:\n{json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def test_predict(product, quantity):
    """Test prediction endpoint"""
    print("\n" + "=" * 70)
    print("🎯 TESTING L1 PRICING PREDICTION")
    print("=" * 70)
    
    payload = {
        "product": product,
        "quantity": quantity
    }
    
    print(f"\n📤 Request:")
    print(json.dumps(payload, indent=2))
    
    response = requests.post(f"{BASE_URL}/api/v1/predict", json=payload)
    
    print(f"\n📥 Response:")
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print("\n✅ SUCCESS!")
        print(json.dumps(result, indent=2))
        
        # Display summary
        print("\n" + "=" * 70)
        print("📊 L1 PRICING SUMMARY")
        print("=" * 70)
        print(f"Product: {result['product']}")
        print(f"Quantity: {result['quantity']}")
        print(f"\n💰 Price Range:")
        print(f"  Low Price  : ₹{result['low_price']:,.2f}")
        print(f"  High Price : ₹{result['high_price']:,.2f}")
        print(f"\n📈 Confidence: {result['confidence']}")
        print(f"👥 Competitors: {result['competitors_analyzed']}")
        
        if result.get('top_competitors'):
            print(f"\n🏆 Top 5 Competitors:")
            for i, comp in enumerate(result['top_competitors'], 1):
                print(f"\n  {i}. {comp['seller_name']}")
                print(f"     Average Bidding Price : ₹{comp['average_bidding_price']:,.2f}")
                print(f"     Inflation Rate       : {comp['inflation_rate_percent']:.2f}%")
                print(f"     Last L1 Price        : ₹{comp['last_l1_price']:,.2f}")
                print(f"     Least Quoted Price   : ₹{comp['least_quoted_price']:,.2f}")
    else:
        print(f"\n❌ ERROR!")
        print(json.dumps(response.json(), indent=2))

if __name__ == "__main__":
    print("\n🚀 L1 PRICING MODEL API - TEST SUITE\n")
    
    # Test 1: Health check
    if test_health():
        print("\n✅ Health check passed!")
    else:
        print("\n❌ Health check failed!")
        exit(1)
    
    # Test 2: Pricing prediction
    test_predict("LIGATION CLIP", 10)
    
    print("\n\n" + "=" * 70)
    print("✅ ALL TESTS COMPLETE")
    print("=" * 70)
