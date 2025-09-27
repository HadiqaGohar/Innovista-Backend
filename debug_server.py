#!/usr/bin/env python3
"""
Debug server issues
"""

import requests
import time

def debug_server():
    """Debug server connectivity and response times"""
    
    print("🔧 Server Debug Check")
    print("=" * 30)
    
    base_url = "http://localhost:8000"
    
    # Test 1: Basic health check
    print("1. Testing health endpoint...")
    try:
        start_time = time.time()
        response = requests.get(f"{base_url}/health", timeout=5)
        end_time = time.time()
        
        if response.status_code == 200:
            print(f"✅ Health check OK ({end_time - start_time:.2f}s)")
        else:
            print(f"❌ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return
    
    # Test 2: Simple API endpoint (not chatbot)
    print("\n2. Testing sessions endpoint...")
    try:
        start_time = time.time()
        response = requests.get(f"{base_url}/api/chatbot/sessions", timeout=15)
        end_time = time.time()
        
        if response.status_code == 200:
            print(f"✅ Sessions endpoint OK ({end_time - start_time:.2f}s)")
            data = response.json()
            print(f"📊 Sessions found: {data.get('total_sessions', 0)}")
        else:
            print(f"❌ Sessions endpoint failed: {response.status_code}")
            print(f"Response: {response.text[:200]}")
    except Exception as e:
        print(f"❌ Sessions endpoint error: {e}")
    
    # Test 3: Simple chatbot message (with longer timeout)
    print("\n3. Testing simple chatbot message...")
    try:
        start_time = time.time()
        response = requests.post(f"{base_url}/api/chatbot", 
                               json={"message": "hello", "session_id": "debug_test"}, 
                               timeout=60)  # Longer timeout
        end_time = time.time()
        
        if response.status_code == 200:
            print(f"✅ Chatbot response OK ({end_time - start_time:.2f}s)")
            result = response.json()
            print(f"📝 Response type: {result.get('type', 'unknown')}")
        else:
            print(f"❌ Chatbot failed: {response.status_code}")
            print(f"Response: {response.text[:200]}")
    except requests.exceptions.Timeout:
        print("❌ Chatbot timeout - agent taking too long to respond")
        print("💡 This might be due to:")
        print("   - Gemini API slow response")
        print("   - Database connection issues")
        print("   - Agent processing taking too long")
    except Exception as e:
        print(f"❌ Chatbot error: {e}")
    
    # Test 4: Database connection test
    print("\n4. Testing database connection...")
    try:
        # Import and test database connection
        import sys
        sys.path.append('.')
        from main import get_db
        
        conn = get_db()
        if conn:
            print("✅ Database connection OK")
            with conn.cursor() as cur:
                cur.execute("SELECT COUNT(*) FROM chat_sessions")
                count = cur.fetchone()[0]
                print(f"📊 Sessions in DB: {count}")
            conn.close()
        else:
            print("❌ Database connection failed")
    except Exception as e:
        print(f"❌ Database test error: {e}")
    
    print("\n" + "=" * 30)
    print("🎯 Debug Complete!")
    print("\n💡 Recommendations:")
    print("- If health check works but chatbot times out: Agent/API issue")
    print("- If database fails: Check TiDB credentials")
    print("- If sessions endpoint fails: Database connection issue")

if __name__ == "__main__":
    debug_server()