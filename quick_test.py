#!/usr/bin/env python3
"""
Quick Test Tool - Simple command line testing
"""

import requests
import json
import sys

def quick_test():
    """Quick test with command line arguments"""
    
    if len(sys.argv) < 2:
        print("🏥 MEDICURA AI - QUICK TEST")
        print("=" * 40)
        print("Usage:")
        print("  python quick_test.py 'your message here'")
        print("  python quick_test.py triage 'chest pain' 'pain,sweating'")
        print("  python quick_test.py history")
        print("  python quick_test.py sessions")
        print("\nExamples:")
        print("  python quick_test.py 'I have a headache'")
        print("  python quick_test.py triage 'chest pain' 'chest pain,shortness of breath'")
        return
    
    base_url = "http://localhost:8000"
    
    # Check server
    try:
        requests.get(f"{base_url}/health", timeout=5)
        print("✅ Server running")
    except:
        print("❌ Server not running - start with: uvicorn main:app --reload")
        return
    
    command = sys.argv[1].lower()
    
    if command == "sessions":
        # Show database sessions
        try:
            response = requests.get(f"{base_url}/api/chatbot/sessions", timeout=10)
            if response.status_code == 200:
                data = response.json()
                print(f"📊 Total Sessions: {data.get('total_sessions', 0)}")
                for session in data.get('sessions', [])[:3]:
                    print(f"  - {session.get('session_id', 'unknown')}: {session.get('message_count', 0)} messages")
            else:
                print(f"❌ Error: {response.status_code}")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    elif command == "triage" and len(sys.argv) >= 4:
        # Triage test
        complaint = sys.argv[2]
        symptoms = sys.argv[3].split(',')
        
        print(f"🚨 TRIAGE TEST: {complaint}")
        print(f"Symptoms: {', '.join(symptoms)}")
        
        try:
            response = requests.post(f"{base_url}/api/health/triage", json={
                "chief_complaint": complaint,
                "symptoms": symptoms,
                "session_id": "quick_test"
            }, timeout=60)
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Triage Level: {result.get('triage_level', 'N/A')}")
                print(f"📊 Urgency Score: {result.get('urgency_score', 'N/A')}/10")
                print(f"🏥 Action: {result.get('routing_decision', 'N/A')}")
            else:
                print(f"❌ Error: {response.status_code}")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    else:
        # Chat message
        message = ' '.join(sys.argv[1:])
        print(f"💬 Testing: {message}")
        
        try:
            response = requests.post(f"{base_url}/api/chatbot", json={
                "message": message,
                "session_id": "quick_test"
            }, timeout=60)
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Response: {result.get('summary', 'No summary')}")
                if result.get('triage_level'):
                    print(f"🚨 Triage: {result.get('triage_level')} ({result.get('urgency_score')}/10)")
            else:
                print(f"❌ Error: {response.status_code}")
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    quick_test()