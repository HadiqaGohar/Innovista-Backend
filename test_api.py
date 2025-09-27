#!/usr/bin/env python3
"""
Quick API test for triage endpoint
"""

import requests
import json

def test_triage_api():
    """Test the triage API endpoint"""
    
    # Test data
    test_data = {
        "chief_complaint": "Severe chest pain",
        "symptoms": ["chest pain", "shortness of breath", "sweating"],
        "duration": "30 minutes",
        "severity": "severe",
        "age": 55,
        "gender": "male",
        "pain_level": 9,
        "additional_info": "Pain radiating to left arm"
    }
    
    try:
        # Test the endpoint
        response = requests.post(
            "http://localhost:8000/api/health/triage",
            json=test_data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ API Test Successful!")
            print(f"Triage Level: {result.get('triage_level')}")
            print(f"Urgency Score: {result.get('urgency_score')}")
            print(f"Routing: {result.get('routing_decision')}")
        else:
            print(f"❌ API Error: {response.status_code}")
            print(response.text)
            
    except requests.exceptions.ConnectionError:
        print("❌ Server not running. Start with: uvicorn main:app --reload")
    except Exception as e:
        print(f"❌ Test error: {e}")

if __name__ == "__main__":
    test_triage_api()