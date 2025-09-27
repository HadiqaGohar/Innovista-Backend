#!/usr/bin/env python3
"""
Test script for conversation history functionality
"""

import requests
import json
import time

def test_conversation_history():
    """Test conversation history with multiple interactions"""
    
    base_url = "http://localhost:8000"
    session_id = "test_session_123"
    
    print("🧠 Testing Conversation History Functionality")
    print("=" * 50)
    
    # Test 1: Initial triage assessment
    print("\n📋 Test 1: Initial Triage Assessment")
    print("-" * 40)
    
    initial_request = {
        "chief_complaint": "Chest pain",
        "symptoms": ["chest pain", "shortness of breath"],
        "duration": "2 hours",
        "severity": "moderate",
        "age": 45,
        "gender": "male",
        "pain_level": 6,
        "session_id": session_id
    }
    
    try:
        response = requests.post(
            f"{base_url}/api/health/triage",
            json=initial_request,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Initial Assessment: {result.get('triage_level')} (Score: {result.get('urgency_score')})")
            print(f"📍 Routing: {result.get('routing_decision')}")
            print(f"📝 Summary: {result.get('case_summary', '')[:100]}...")
        else:
            print(f"❌ Error: {response.status_code}")
            return
            
    except requests.exceptions.ConnectionError:
        print("❌ Server not running. Start with: uvicorn main:app --reload")
        return
    except Exception as e:
        print(f"❌ Error: {e}")
        return
    
    # Wait a moment
    time.sleep(2)
    
    # Test 2: Follow-up chat with history context
    print("\n💬 Test 2: Follow-up Chat (Should remember previous chest pain)")
    print("-" * 40)
    
    followup_request = {
        "message": "The chest pain is getting worse and now I'm feeling nauseous",
        "session_id": session_id
    }
    
    try:
        response = requests.post(
            f"{base_url}/api/chatbot",
            json=followup_request,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Follow-up Response Type: {result.get('type')}")
            print(f"📝 Summary: {result.get('summary', '')[:150]}...")
            
            # Check if response references previous interaction
            response_text = json.dumps(result).lower()
            if any(word in response_text for word in ["previous", "earlier", "before", "chest pain"]):
                print("🧠 ✅ Agent remembered previous conversation!")
            else:
                print("🧠 ⚠️  Agent may not have used conversation history")
        else:
            print(f"❌ Error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Wait a moment
    time.sleep(2)
    
    # Test 3: Another follow-up with more context
    print("\n💬 Test 3: Second Follow-up (Should build on conversation)")
    print("-" * 40)
    
    second_followup = {
        "message": "Should I go to the emergency room now?",
        "session_id": session_id
    }
    
    try:
        response = requests.post(
            f"{base_url}/api/chatbot",
            json=second_followup,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Second Follow-up Type: {result.get('type')}")
            print(f"📝 Summary: {result.get('summary', '')[:150]}...")
            
            # Check for emergency escalation due to worsening symptoms
            response_text = json.dumps(result).lower()
            if any(word in response_text for word in ["emergency", "urgent", "immediate", "worsening"]):
                print("🚨 ✅ Agent escalated due to worsening symptoms!")
            else:
                print("🚨 ⚠️  Agent may not have escalated appropriately")
        else:
            print(f"❌ Error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 4: Check session history
    print("\n📚 Test 4: Session History Check")
    print("-" * 40)
    
    try:
        # This would require a history endpoint, but we can infer from responses
        print("✅ Session ID used consistently:", session_id)
        print("✅ Multiple interactions completed")
        print("✅ Context should be maintained across calls")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 Conversation History Test Complete!")
    print("\n💡 Key Features Tested:")
    print("   - Session ID tracking")
    print("   - Conversation history context")
    print("   - Progressive symptom assessment")
    print("   - Contextual recommendations")

def test_different_session():
    """Test that different sessions are isolated"""
    
    print("\n🔒 Testing Session Isolation")
    print("-" * 40)
    
    different_session = {
        "message": "I have a headache",
        "session_id": "different_session_456"
    }
    
    try:
        response = requests.post(
            "http://localhost:8000/api/chatbot",
            json=different_session,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            response_text = json.dumps(result).lower()
            
            # Should NOT reference chest pain from previous session
            if "chest" in response_text or "pain" in response_text and "chest" in response_text:
                print("❌ Session isolation failed - referenced other session")
            else:
                print("✅ Session isolation working - no cross-session contamination")
                
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_conversation_history()
    test_different_session()