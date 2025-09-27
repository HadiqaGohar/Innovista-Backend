#!/usr/bin/env python3
"""
Quick History Check - Simple command to check if history is working
"""

import requests
import json

def quick_check():
    """Quick check for history functionality"""
    
    print("🔍 Quick History Check")
    print("=" * 30)
    
    base_url = "http://localhost:8000"
    
    # Check 1: Server running?
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        print("✅ Server is running")
    except:
        print("❌ Server not running - start with: uvicorn main:app --reload")
        return
    
    # Check 2: Any sessions exist?
    try:
        response = requests.get(f"{base_url}/api/chatbot/sessions", timeout=10)
        if response.status_code == 200:
            data = response.json()
            total = data.get('total_sessions', 0)
            print(f"📊 Total sessions in database: {total}")
            
            if total > 0:
                print("✅ History is being saved!")
                sessions = data.get('sessions', [])[:3]  # Show first 3
                for session in sessions:
                    session_id = session.get('session_id', 'unknown')
                    message_count = session.get('message_count', 0)
                    print(f"   - {session_id}: {message_count} messages")
            else:
                print("⚠️  No sessions found - try sending some messages first")
        else:
            print(f"❌ Error checking sessions: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Check 3: Test a quick conversation
    print("\n🧪 Testing new conversation...")
    test_session = "quick_test_session"
    
    try:
        # Send test message
        response = requests.post(f"{base_url}/api/chatbot", json={
            "message": "Test message for history",
            "session_id": test_session
        }, timeout=30)
        
        if response.status_code == 200:
            print("✅ Test message sent")
            
            # Check if it was saved
            response = requests.get(f"{base_url}/api/chatbot/session/{test_session}/history", timeout=10)
            if response.status_code == 200:
                history_data = response.json()
                message_count = history_data.get('total_messages', 0)
                if message_count > 0:
                    print(f"✅ History saved! ({message_count} messages)")
                else:
                    print("❌ History not saved")
            else:
                print("❌ Could not retrieve history")
        else:
            print(f"❌ Test message failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Test error: {e}")
    
    print("\n" + "=" * 30)
    print("🎯 Quick Check Complete!")

if __name__ == "__main__":
    quick_check()