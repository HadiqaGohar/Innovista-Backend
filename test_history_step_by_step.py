#!/usr/bin/env python3
"""
Step-by-step history testing guide
"""

import requests
import json
import time

def test_history_step_by_step():
    """Step by step history testing"""
    
    base_url = "http://localhost:8000"
    test_session = "test_history_session_001"
    
    print("🧪 Step-by-Step History Testing")
    print("=" * 50)
    
    print("\n📋 Step 1: Check if server is running")
    print("-" * 30)
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Server is running!")
        else:
            print("❌ Server responded with error")
            return
    except:
        print("❌ Server is not running!")
        print("💡 Start server with: uvicorn main:app --reload")
        return
    
    print("\n📋 Step 2: Send first message")
    print("-" * 30)
    first_message = {
        "message": "I have chest pain",
        "session_id": test_session
    }
    
    try:
        response = requests.post(f"{base_url}/api/chatbot", json=first_message, timeout=30)
        if response.status_code == 200:
            result = response.json()
            print("✅ First message sent successfully!")
            print(f"📝 Response type: {result.get('type', 'unknown')}")
            print(f"📝 Summary: {result.get('summary', 'No summary')[:100]}...")
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.text)
            return
    except Exception as e:
        print(f"❌ Error: {e}")
        return
    
    time.sleep(2)
    
    print("\n📋 Step 3: Send follow-up message")
    print("-" * 30)
    second_message = {
        "message": "The chest pain is getting worse and I'm sweating",
        "session_id": test_session  # Same session ID
    }
    
    try:
        response = requests.post(f"{base_url}/api/chatbot", json=second_message, timeout=30)
        if response.status_code == 200:
            result = response.json()
            print("✅ Follow-up message sent successfully!")
            print(f"📝 Response type: {result.get('type', 'unknown')}")
            print(f"📝 Summary: {result.get('summary', 'No summary')[:100]}...")
        else:
            print(f"❌ Error: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Error: {e}")
        return
    
    time.sleep(2)
    
    print("\n📋 Step 4: Check conversation history via API")
    print("-" * 30)
    try:
        response = requests.get(f"{base_url}/api/chatbot/session/{test_session}/history", timeout=10)
        if response.status_code == 200:
            history_data = response.json()
            print("✅ History retrieved successfully!")
            print(f"📊 Total messages: {history_data.get('total_messages', 0)}")
            
            history = history_data.get('history', [])
            if history:
                print("\n💬 Conversation History:")
                for i, msg in enumerate(history, 1):
                    role = msg.get('role', 'unknown').upper()
                    content = msg.get('content', '')[:100]
                    timestamp = msg.get('timestamp', 'no time')
                    print(f"{i}. [{role}] {timestamp}")
                    print(f"   {content}...")
                    if msg.get('triage_level'):
                        print(f"   🚨 Triage: {msg.get('triage_level')} (Score: {msg.get('urgency_score', 'N/A')})")
                    print()
            else:
                print("❌ No history found!")
        else:
            print(f"❌ Error getting history: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n📋 Step 5: Check all sessions")
    print("-" * 30)
    try:
        response = requests.get(f"{base_url}/api/chatbot/sessions", timeout=10)
        if response.status_code == 200:
            sessions_data = response.json()
            print("✅ Sessions retrieved successfully!")
            print(f"📊 Total sessions: {sessions_data.get('total_sessions', 0)}")
            
            sessions = sessions_data.get('sessions', [])
            if sessions:
                print("\n📋 All Sessions:")
                for i, session in enumerate(sessions[:5], 1):  # Show first 5
                    session_id = session.get('session_id', 'unknown')
                    message_count = session.get('message_count', 0)
                    last_updated = session.get('last_updated', 'unknown')
                    print(f"{i}. {session_id}")
                    print(f"   Messages: {message_count}, Last: {last_updated}")
                    print()
        else:
            print(f"❌ Error getting sessions: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n📋 Step 6: Test with different session (should be isolated)")
    print("-" * 30)
    different_session = {
        "message": "I have a headache",
        "session_id": "different_session_002"
    }
    
    try:
        response = requests.post(f"{base_url}/api/chatbot", json=different_session, timeout=30)
        if response.status_code == 200:
            result = response.json()
            print("✅ Different session message sent!")
            
            # Check if it mentions chest pain (it shouldn't)
            response_text = json.dumps(result).lower()
            if "chest" in response_text:
                print("❌ Session isolation failed - mentioned chest pain")
            else:
                print("✅ Session isolation working - no cross-contamination")
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 History Testing Complete!")
    print("\n📊 Summary:")
    print("✅ If you see conversation history above, it's working!")
    print("✅ Messages should be stored with timestamps")
    print("✅ Different sessions should be isolated")
    print("✅ API endpoints for viewing history are working")
    
    print(f"\n🔗 Direct Links:")
    print(f"📖 View history: {base_url}/api/chatbot/session/{test_session}/history")
    print(f"📋 All sessions: {base_url}/api/chatbot/sessions")
    print(f"📚 API docs: {base_url}/api/docs")

if __name__ == "__main__":
    test_history_step_by_step()