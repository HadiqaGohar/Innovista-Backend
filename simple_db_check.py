#!/usr/bin/env python3
"""
Simple database check without API calls
"""

def check_database_directly():
    """Check database connection and history table directly"""
    
    print("🗄️ Direct Database Check")
    print("=" * 30)
    
    try:
        # Import database functions
        import sys
        sys.path.append('.')
        from main import get_db
        import json
        
        # Test connection
        print("1. Testing database connection...")
        conn = get_db()
        if not conn:
            print("❌ Database connection failed")
            return
        
        print("✅ Database connected successfully")
        
        # Check table exists
        print("\n2. Checking chat_sessions table...")
        with conn.cursor() as cur:
            cur.execute("SHOW TABLES LIKE 'chat_sessions'")
            result = cur.fetchone()
            
            if result:
                print("✅ chat_sessions table exists")
                
                # Count sessions
                cur.execute("SELECT COUNT(*) FROM chat_sessions")
                count = cur.fetchone()[0]
                print(f"📊 Total sessions: {count}")
                
                if count > 0:
                    # Show recent sessions
                    cur.execute("SELECT session_id, last_updated FROM chat_sessions ORDER BY last_updated DESC LIMIT 3")
                    sessions = cur.fetchall()
                    print("\n📋 Recent sessions:")
                    for session_id, last_updated in sessions:
                        print(f"   - {session_id}: {last_updated}")
                else:
                    print("⚠️  No sessions found - history not being saved yet")
            else:
                print("❌ chat_sessions table does not exist")
                print("💡 Table should be created automatically when server starts")
        
        conn.close()
        
        # Test save/load functions
        print("\n3. Testing history functions...")
        from main import load_history, save_history
        
        # Test load (should return empty list for new session)
        test_session = "test_db_check"
        history = load_history(test_session)
        print(f"✅ load_history works: {len(history)} messages")
        
        # Test save
        test_history = [
            {"role": "user", "content": "test message", "timestamp": "2024-01-01T00:00:00"},
            {"role": "assistant", "content": "test response", "timestamp": "2024-01-01T00:00:01"}
        ]
        
        save_history(test_session, test_history)
        print("✅ save_history works")
        
        # Verify save worked
        loaded_history = load_history(test_session)
        print(f"✅ History saved and loaded: {len(loaded_history)} messages")
        
        print("\n" + "=" * 30)
        print("🎯 Database Check Complete!")
        
        if count == 0:
            print("\n💡 Next Steps:")
            print("1. Send a message via API to create first session")
            print("2. Check if agents are responding properly")
            print("3. Verify Gemini API key is working")
        else:
            print("\n✅ Database is working correctly!")
            print("💡 If API calls timeout, it's likely an agent response issue")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure you're in the correct directory")
    except Exception as e:
        print(f"❌ Database error: {e}")
        print("💡 Check your database credentials in .env file")

if __name__ == "__main__":
    check_database_directly()