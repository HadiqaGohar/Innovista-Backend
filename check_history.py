#!/usr/bin/env python3
"""
History Checker - Check if conversation history is being saved properly
"""

import pymysql
import json
import os
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

# TiDB Configuration
DB_CONFIG = {
    "host": os.getenv("TIDB_HOST", "gateway01.us-west-2.prod.aws.tidbcloud.com"),
    "port": 4000,
    "user": os.getenv("TIDB_USERNAME", "34oY1b3G6arXWAM.root"),
    "password": os.getenv("TIDB_PASSWORD", "M9iWYjgizxiiT1qh"),
    "database": os.getenv("TIDB_DATABASE", "test"),
    "charset": "utf8mb4",
    "ssl": {"ssl_mode": "VERIFY_IDENTITY"}
}

def get_db():
    """Establish a connection to TiDB."""
    try:
        connection = pymysql.connect(**DB_CONFIG)
        return connection
    except pymysql.err.OperationalError as e:
        print(f"❌ Database connection failed: {str(e)}")
        return None

def check_history_table():
    """Check if history table exists and show structure"""
    print("🔍 Checking History Table Structure")
    print("=" * 50)
    
    conn = get_db()
    if not conn:
        return False
    
    try:
        with conn.cursor() as cur:
            # Check if table exists
            cur.execute("SHOW TABLES LIKE 'chat_sessions'")
            result = cur.fetchone()
            
            if result:
                print("✅ chat_sessions table exists")
                
                # Show table structure
                cur.execute("DESCRIBE chat_sessions")
                columns = cur.fetchall()
                print("\n📋 Table Structure:")
                for col in columns:
                    print(f"   - {col[0]}: {col[1]}")
                
                # Count total sessions
                cur.execute("SELECT COUNT(*) FROM chat_sessions")
                count = cur.fetchone()[0]
                print(f"\n📊 Total Sessions: {count}")
                
                return True
            else:
                print("❌ chat_sessions table does not exist")
                return False
                
    except Exception as e:
        print(f"❌ Error checking table: {e}")
        return False
    finally:
        conn.close()

def view_all_sessions():
    """View all conversation sessions"""
    print("\n💬 All Conversation Sessions")
    print("=" * 50)
    
    conn = get_db()
    if not conn:
        return
    
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT session_id, last_updated FROM chat_sessions ORDER BY last_updated DESC")
            sessions = cur.fetchall()
            
            if sessions:
                print(f"Found {len(sessions)} sessions:")
                for i, (session_id, last_updated) in enumerate(sessions, 1):
                    print(f"{i}. Session: {session_id}")
                    print(f"   Last Updated: {last_updated}")
                    print()
            else:
                print("No sessions found in database")
                
    except Exception as e:
        print(f"❌ Error viewing sessions: {e}")
    finally:
        conn.close()

def view_session_history(session_id):
    """View history for a specific session"""
    print(f"\n📖 Session History: {session_id}")
    print("=" * 50)
    
    conn = get_db()
    if not conn:
        return
    
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT history, last_updated FROM chat_sessions WHERE session_id = %s", (session_id,))
            result = cur.fetchone()
            
            if result:
                history_json, last_updated = result
                history = json.loads(history_json)
                
                print(f"📅 Last Updated: {last_updated}")
                print(f"💬 Total Messages: {len(history)}")
                print("\n🗣️ Conversation:")
                print("-" * 30)
                
                for i, msg in enumerate(history, 1):
                    role = msg.get('role', 'unknown')
                    content = msg.get('content', '')
                    timestamp = msg.get('timestamp', 'no timestamp')
                    
                    # Truncate long content
                    if len(content) > 200:
                        content = content[:200] + "..."
                    
                    print(f"{i}. [{role.upper()}] {timestamp}")
                    print(f"   {content}")
                    print()
                    
            else:
                print(f"❌ No history found for session: {session_id}")
                
    except Exception as e:
        print(f"❌ Error viewing session history: {e}")
    finally:
        conn.close()

def create_test_session():
    """Create a test session to verify saving works"""
    print("\n🧪 Creating Test Session")
    print("=" * 50)
    
    conn = get_db()
    if not conn:
        return
    
    test_session_id = f"test_session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    test_history = [
        {
            "role": "user",
            "content": "I have a headache",
            "timestamp": datetime.now().isoformat()
        },
        {
            "role": "assistant", 
            "content": json.dumps({
                "summary": "Headache assessment",
                "triage_level": "MEDIUM",
                "urgency_score": 4
            }),
            "timestamp": datetime.now().isoformat()
        }
    ]
    
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO chat_sessions (session_id, history)
                VALUES (%s, %s)
                ON DUPLICATE KEY UPDATE history = %s, last_updated = CURRENT_TIMESTAMP
            """, (test_session_id, json.dumps(test_history), json.dumps(test_history)))
            conn.commit()
            
        print(f"✅ Test session created: {test_session_id}")
        print("✅ History saving is working!")
        
        # Verify it was saved
        view_session_history(test_session_id)
        
    except Exception as e:
        print(f"❌ Error creating test session: {e}")
    finally:
        conn.close()

def interactive_menu():
    """Interactive menu for checking history"""
    while True:
        print("\n🏥 Medicura History Checker")
        print("=" * 30)
        print("1. Check table structure")
        print("2. View all sessions")
        print("3. View specific session")
        print("4. Create test session")
        print("5. Exit")
        
        choice = input("\nSelect option (1-5): ").strip()
        
        if choice == "1":
            check_history_table()
        elif choice == "2":
            view_all_sessions()
        elif choice == "3":
            session_id = input("Enter session ID: ").strip()
            if session_id:
                view_session_history(session_id)
            else:
                print("❌ Please enter a valid session ID")
        elif choice == "4":
            create_test_session()
        elif choice == "5":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid option. Please select 1-5.")

def main():
    """Main function"""
    print("🔍 Medicura Conversation History Checker")
    print("=" * 50)
    
    # Quick check
    if check_history_table():
        view_all_sessions()
        
        # Interactive menu
        print("\n" + "=" * 50)
        interactive_menu()
    else:
        print("\n❌ Cannot proceed without database table")
        print("💡 Make sure your server has run at least once to create tables")

if __name__ == "__main__":
    main()