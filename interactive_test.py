#!/usr/bin/env python3
"""
Interactive Testing Tool - Test Medicura AI with your own inputs
"""

import requests
import json
import time
from datetime import datetime

class MedicuraInteractiveTester:
    def __init__(self):
        self.base_url = "http://localhost:8000"
        self.session_id = f"interactive_test_{int(time.time())}"
        self.conversation_history = []
    
    def print_header(self):
        print("🏥 MEDICURA AI - INTERACTIVE TESTER")
        print("=" * 50)
        print(f"Session ID: {self.session_id}")
        print("Commands: 'quit' to exit, 'history' to see conversation")
        print("=" * 50)
    
    def check_server(self):
        """Check if server is running"""
        try:
            response = requests.get(f"{self.base_url}/health", timeout=5)
            if response.status_code == 200:
                print("✅ Server is running!")
                return True
            else:
                print(f"❌ Server error: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Server not running: {e}")
            print("💡 Start server with: uvicorn main:app --reload")
            return False
    
    def send_message(self, message):
        """Send message to chatbot"""
        print(f"\n👤 You: {message}")
        print("🤖 Medicura AI is thinking...")
        
        try:
            start_time = time.time()
            response = requests.post(
                f"{self.base_url}/api/chatbot",
                json={
                    "message": message,
                    "session_id": self.session_id
                },
                timeout=60  # 60 second timeout
            )
            end_time = time.time()
            
            if response.status_code == 200:
                result = response.json()
                response_time = end_time - start_time
                
                print(f"✅ Response received ({response_time:.2f}s)")
                print("-" * 40)
                
                # Display response
                summary = result.get('summary', 'No summary')
                triage_level = result.get('triage_level', '')
                urgency_score = result.get('urgency_score', '')
                response_type = result.get('type', 'general')
                
                print(f"🤖 Medicura AI ({response_type}):")
                print(f"📝 {summary}")
                
                if triage_level:
                    print(f"🚨 Triage Level: {triage_level}")
                    print(f"📊 Urgency Score: {urgency_score}/10")
                
                if result.get('recommendations'):
                    print("💡 Recommendations:")
                    for i, rec in enumerate(result['recommendations'][:3], 1):
                        print(f"   {i}. {rec}")
                
                if result.get('when_to_seek_help'):
                    print("⚠️  Seek help if:")
                    for i, help_item in enumerate(result['when_to_seek_help'][:2], 1):
                        print(f"   {i}. {help_item}")
                
                # Store in conversation history
                self.conversation_history.append({
                    'user': message,
                    'assistant': summary,
                    'triage_level': triage_level,
                    'urgency_score': urgency_score,
                    'timestamp': datetime.now().strftime('%H:%M:%S')
                })
                
                return True
            else:
                print(f"❌ Error: {response.status_code}")
                print(f"Response: {response.text}")
                return False
                
        except requests.exceptions.Timeout:
            print("❌ Request timed out (60s)")
            print("💡 The AI might be processing a complex query")
            return False
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    
    def send_triage_request(self, complaint, symptoms):
        """Send dedicated triage request"""
        print(f"\n🚨 TRIAGE REQUEST")
        print(f"Chief Complaint: {complaint}")
        print(f"Symptoms: {', '.join(symptoms)}")
        print("🤖 Analyzing urgency...")
        
        try:
            response = requests.post(
                f"{self.base_url}/api/health/triage",
                json={
                    "chief_complaint": complaint,
                    "symptoms": symptoms,
                    "session_id": self.session_id
                },
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                print("✅ Triage Assessment Complete")
                print("-" * 40)
                
                print(f"🚨 Triage Level: {result.get('triage_level', 'N/A')}")
                print(f"📊 Urgency Score: {result.get('urgency_score', 'N/A')}/10")
                print(f"🏥 Recommended Action: {result.get('routing_decision', 'N/A')}")
                print(f"⏰ Time Frame: {result.get('time_frame', 'N/A')}")
                print(f"📝 Assessment: {result.get('case_summary', 'N/A')}")
                
                if result.get('red_flags'):
                    print(f"🚩 Red Flags: {', '.join(result['red_flags'])}")
                
                return True
            else:
                print(f"❌ Triage Error: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Triage Error: {e}")
            return False
    
    def show_history(self):
        """Show conversation history"""
        if not self.conversation_history:
            print("📝 No conversation history yet")
            return
        
        print(f"\n📚 CONVERSATION HISTORY ({len(self.conversation_history)} exchanges)")
        print("=" * 50)
        
        for i, exchange in enumerate(self.conversation_history, 1):
            print(f"\n{i}. [{exchange['timestamp']}]")
            print(f"👤 You: {exchange['user']}")
            print(f"🤖 AI: {exchange['assistant'][:100]}...")
            if exchange['triage_level']:
                print(f"🚨 Triage: {exchange['triage_level']} ({exchange['urgency_score']}/10)")
    
    def show_menu(self):
        """Show interactive menu"""
        print("\n" + "=" * 50)
        print("🎯 WHAT WOULD YOU LIKE TO TEST?")
        print("=" * 50)
        print("1. 💬 Send Chat Message")
        print("2. 🚨 Triage Assessment")
        print("3. 📚 View Conversation History")
        print("4. 🔍 Check Database Sessions")
        print("5. ❌ Exit")
        print("-" * 50)
    
    def check_database_sessions(self):
        """Check database sessions via API"""
        try:
            response = requests.get(f"{self.base_url}/api/chatbot/sessions", timeout=10)
            if response.status_code == 200:
                data = response.json()
                total = data.get('total_sessions', 0)
                print(f"\n📊 DATABASE SESSIONS: {total}")
                print("-" * 30)
                
                sessions = data.get('sessions', [])[:5]
                for i, session in enumerate(sessions, 1):
                    session_id = session.get('session_id', 'unknown')
                    message_count = session.get('message_count', 0)
                    last_updated = session.get('last_updated', 'unknown')
                    print(f"{i}. {session_id[:20]}...")
                    print(f"   Messages: {message_count}, Updated: {last_updated}")
                
                return True
            else:
                print(f"❌ Database check failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Database check error: {e}")
            return False
    
    def run(self):
        """Main interactive loop"""
        self.print_header()
        
        if not self.check_server():
            return
        
        while True:
            self.show_menu()
            choice = input("Select option (1-5): ").strip()
            
            if choice == "1":
                message = input("\n💬 Enter your message: ").strip()
                if message:
                    self.send_message(message)
                else:
                    print("❌ Please enter a message")
            
            elif choice == "2":
                complaint = input("\n🚨 Chief complaint: ").strip()
                symptoms_input = input("🔍 Symptoms (comma separated): ").strip()
                
                if complaint and symptoms_input:
                    symptoms = [s.strip() for s in symptoms_input.split(',')]
                    self.send_triage_request(complaint, symptoms)
                else:
                    print("❌ Please enter complaint and symptoms")
            
            elif choice == "3":
                self.show_history()
            
            elif choice == "4":
                self.check_database_sessions()
            
            elif choice == "5":
                print("\n👋 Thanks for testing Medicura AI!")
                break
            
            else:
                print("❌ Invalid option. Please select 1-5.")

if __name__ == "__main__":
    tester = MedicuraInteractiveTester()
    tester.run()