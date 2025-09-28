# import streamlit as st
# import requests
# import json
# import uuid
# from datetime import datetime
# import pandas as pd
# import time
# import os
# from typing import List, Dict, Any, Optional

# # Page configuration
# st.set_page_config(
#     page_title="Medicura AI Health Assistant",
#     page_icon="🏥",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # Custom CSS for professional medical UI
# st.markdown("""
# <style>
#     .main-header {
#         font-size: 2.5rem;
#         color: #2563eb;
#         text-align: center;
#         margin-bottom: 1rem;
#         font-weight: bold;
#     }
#     .sub-header {
#         font-size: 1.4rem;
#         color: #dc2626;
#         margin-bottom: 1rem;
#         font-weight: 600;
#     }
#     .card {
#         background-color: #f8fafc;
#         padding: 20px;
#         border-radius: 10px;
#         border-left: 5px solid #2563eb;
#         margin: 10px 0;
#         box-shadow: 0 2px 4px rgba(0,0,0,0.1);
#     }
#     .emergency-card {
#         background-color: #fef2f2;
#         border-left: 5px solid #dc2626;
#     }
#     .success-card {
#         background-color: #f0fdf4;
#         border-left: 5px solid #16a34a;
#     }
#     .chat-user {
#         background: linear-gradient(135deg, #2563eb, #1d4ed8);
#         color: white;
#         padding: 12px 16px;
#         border-radius: 15px 15px 5px 15px;
#         margin: 8px 0;
#         max-width: 80%;
#         margin-left: auto;
#     }
#     .chat-assistant {
#         background: linear-gradient(135deg, #f3f4f6, #e5e7eb);
#         color: #1f2937;
#         padding: 12px 16px;
#         border-radius: 15px 15px 15px 5px;
#         margin: 8px 0;
#         max-width: 80%;
#         margin-right: auto;
#         border: 1px solid #d1d5db;
#     }
#     .specialty-btn {
#         background: linear-gradient(135deg, #ec4899, #db2777);
#         color: white;
#         padding: 12px;
#         border-radius: 8px;
#         margin: 5px;
#         border: none;
#         cursor: pointer;
#         transition: all 0.3s;
#     }
#     .specialty-btn:hover {
#         transform: translateY(-2px);
#         box-shadow: 0 4px 8px rgba(0,0,0,0.2);
#     }
#     .feature-card {
#         background: white;
#         padding: 20px;
#         border-radius: 10px;
#         border: 2px solid #e5e7eb;
#         margin: 10px;
#         text-align: center;
#         transition: all 0.3s;
#     }
#     .feature-card:hover {
#         border-color: #2563eb;
#         transform: translateY(-3px);
#     }
# </style>
# """, unsafe_allow_html=True)

# # Backend API configuration - Replace with your actual backend URL
# BACKEND_URL = "https://hg-medicura-ai-backend-production.up.railway.app"

# class MedicuraAPIClient:
#     def __init__(self, base_url: str):
#         self.base_url = base_url
#         self.timeout = 30
    
#     def _make_request(self, endpoint: str, payload: Dict = None, method: str = "POST"):
#         """Generic request handler"""
#         url = f"{self.base_url}{endpoint}"
#         try:
#             if method == "POST":
#                 response = requests.post(url, json=payload, timeout=self.timeout)
#             else:
#                 response = requests.get(url, params=payload, timeout=self.timeout)
            
#             if response.status_code == 200:
#                 return response.json()
#             else:
#                 st.error(f"API Error: Status {response.status_code}")
#                 return None
#         except Exception as e:
#             st.error(f"Connection Error: {str(e)}")
#             return None
    
#     # Chatbot endpoints
#     def send_chat_message(self, message: str, session_id: str = None) -> Optional[Dict]:
#         """Send message to main chatbot"""
#         endpoint = "/api/chatbot"
#         payload = {"message": message, "session_id": session_id}
#         return self._make_request(endpoint, payload)
    
#     def clear_session(self, session_id: str) -> bool:
#         """Clear chat session"""
#         endpoint = "/api/chatbot/session/clear"
#         payload = {"session_id": session_id}
#         result = self._make_request(endpoint, payload)
#         return result is not None
    
#     def get_session_history(self, session_id: str) -> Optional[Dict]:
#         """Get session history"""
#         endpoint = f"/api/chatbot/session/{session_id}/history"
#         return self._make_request(endpoint, method="GET")
    
#     # Health endpoints
#     def analyze_symptoms(self, symptoms: List[str], duration: str = None, severity: str = None) -> Optional[Dict]:
#         """Analyze symptoms"""
#         endpoint = "/api/health/symptom-analyzer"
#         payload = {
#             "symptoms": symptoms,
#             "duration": duration or "not specified",
#             "severity": severity or "not specified"
#         }
#         return self._make_request(endpoint, payload)
    
#     def check_drug_interactions(self, medications: List[str], age: int = None, 
#                                gender: str = None, conditions: List[str] = None, 
#                                other_meds: List[str] = None) -> Optional[Dict]:
#         """Check drug interactions"""
#         endpoint = "/api/health/drug-interactions"
#         payload = {
#             "medications": medications,
#             "age": age,
#             "gender": gender,
#             "existing_conditions": conditions or [],
#             "other_medications": other_meds or []
#         }
#         return self._make_request(endpoint, payload)
    
#     def explain_medical_term(self, term: str, language: str = "en") -> Optional[Dict]:
#         """Explain medical term"""
#         endpoint = "/api/health/medical-term"
#         payload = {"term": term, "language": language}
#         return self._make_request(endpoint, payload)
    
#     def triage_assessment(self, triage_data: Dict) -> Optional[Dict]:
#         """Perform triage assessment"""
#         endpoint = "/api/health/triage"
#         return self._make_request(endpoint, triage_data)
    
#     def summarize_report(self, text: str, language: str = "en") -> Optional[Dict]:
#         """Summarize medical report"""
#         endpoint = "/api/health/report-summarize"
#         payload = {"text": text, "language": language}
#         return self._make_request(endpoint, payload)
    
#     # Booking endpoint
#     def book_appointment(self, name: str, service: str, contact: str) -> Optional[Dict]:
#         """Book appointment"""
#         endpoint = "/book"
#         payload = {
#             "citizen_name": name,
#             "service": service,
#             "contact": contact
#         }
#         return self._make_request(endpoint, payload)
    
#     # Specialist consultation
#     def consult_specialist(self, specialist_type: str, query: str, session_id: str = None) -> Optional[Dict]:
#         """Consult with specialist"""
#         endpoint = "/api/specialist/consult"
#         payload = {
#             "specialist_type": specialist_type,
#             "query": query,
#             "session_id": session_id
#         }
#         return self._make_request(endpoint, payload)
    
#     # Test endpoints
#     def test_connection(self) -> bool:
#         """Test backend connection"""
#         endpoint = "/health"
#         result = self._make_request(endpoint, method="GET")
#         return result is not None and result.get("status") == "healthy"

# # Initialize API client
# api_client = MedicuraAPIClient(BACKEND_URL)

# def initialize_session_state():
#     """Initialize all session state variables"""
#     if 'session_id' not in st.session_state:
#         st.session_state.session_id = str(uuid.uuid4())
#     if 'chat_history' not in st.session_state:
#         st.session_state.chat_history = []
#     if 'current_page' not in st.session_state:
#         st.session_state.current_page = "Dashboard"
#     if 'specialist_type' not in st.session_state:
#         st.session_state.specialist_type = "General"
#     if 'api_connected' not in st.session_state:
#         st.session_state.api_connected = False

# def test_api_connection():
#     """Test connection to backend API"""
#     with st.spinner("Testing connection to Medicura AI Backend..."):
#         if api_client.test_connection():
#             st.session_state.api_connected = True
#             return True
#         else:
#             st.session_state.api_connected = False
#             return False

# def display_chat_message(role: str, content: Any, timestamp: str = None):
#     """Display chat message with appropriate styling"""
#     if role == "user":
#         st.markdown(f"""
#         <div class="chat-user">
#             <strong>You:</strong> {content}<br>
#             <small>{timestamp if timestamp else datetime.now().strftime('%H:%M')}</small>
#         </div>
#         """, unsafe_allow_html=True)
#     else:
#         try:
#             if isinstance(content, str):
#                 response_data = json.loads(content)
#             else:
#                 response_data = content
            
#             summary = response_data.get('summary', 'No summary available')
#             detailed_analysis = response_data.get('detailed_analysis', '')
#             recommendations = response_data.get('recommendations', [])
#             when_to_seek_help = response_data.get('when_to_seek_help', [])
#             triage_level = response_data.get('triage_level', '')
            
#             # Display main response
#             st.markdown(f"""
#             <div class="chat-assistant">
#                 <strong>Medicura AI:</strong> {summary}<br>
#                 <small>{timestamp if timestamp else datetime.now().strftime('%H:%M')}</small>
#             </div>
#             """, unsafe_allow_html=True)
            
#             # Display additional information in expandable section
#             with st.expander("📋 View Detailed Analysis", expanded=False):
#                 if detailed_analysis and detailed_analysis != summary:
#                     st.markdown("**Detailed Analysis:**")
#                     st.write(detailed_analysis)
                
#                 if triage_level:
#                     st.markdown(f"**Triage Level:** 🚨 {triage_level.upper()}")
                
#                 if recommendations:
#                     st.markdown("**Recommendations:**")
#                     for i, rec in enumerate(recommendations, 1):
#                         st.write(f"• {rec}")
                
#                 if when_to_seek_help:
#                     st.markdown("**When to Seek Help:**")
#                     for i, when in enumerate(when_to_seek_help, 1):
#                         st.write(f"• {when}")
                        
#         except json.JSONDecodeError:
#             st.markdown(f"""
#             <div class="chat-assistant">
#                 <strong>Medicura AI:</strong> {content}<br>
#                 <small>{timestamp if timestamp else datetime.now().strftime('%H:%M')}</small>
#             </div>
#             """, unsafe_allow_html=True)

# def render_dashboard():
#     """Render main dashboard"""
#     st.markdown('<div class="main-header">🏥 Medicura AI Health Assistant</div>', unsafe_allow_html=True)
    
#     # Connection status
#     col1, col2, col3 = st.columns([2, 1, 1])
#     with col2:
#         status_color = "🟢" if st.session_state.api_connected else "🔴"
#         st.write(f"{status_color} Backend: {'Connected' if st.session_state.api_connected else 'Disconnected'}")
    
#     # Emergency banner
#     st.markdown("""
#     <div class="card emergency-card">
#         <h3>🚨 Emergency Notice</h3>
#         <p>If you are experiencing a medical emergency, please call your local emergency number immediately. 
#         This AI assistant is for informational purposes only and cannot provide emergency medical care.</p>
#     </div>
#     """, unsafe_allow_html=True)
    
#     # Feature cards
#     st.markdown("### 🚀 Quick Access Features")
    
#     cols = st.columns(4)
#     features = [
#         ("🤖 AI Chatbot", "General health conversations"),
#         ("🔍 Symptom Check", "Analyze your symptoms"), 
#         ("💊 Drug Check", "Medication interactions"),
#         ("📚 Medical Terms", "Understand medical jargon")
#     ]
    
#     for i, (title, desc) in enumerate(features):
#         with cols[i]:
#             if st.button(f"**{title}**\n\n{desc}", use_container_width=True, key=f"feature_{i}"):
#                 st.session_state.current_page = title.split()[-1]
#                 st.rerun()
    
#     # Recent chat preview
#     if st.session_state.chat_history:
#         st.markdown("### 💬 Recent Conversation")
#         recent_messages = st.session_state.chat_history[-3:]  # Last 3 messages
#         for msg in recent_messages:
#             display_chat_message(msg['role'], msg['content'], msg.get('timestamp'))

# def render_chatbot():
#     """Render AI chatbot interface"""
#     st.markdown('<div class="main-header">🤖 Medicura AI Chatbot</div>', unsafe_allow_html=True)
    
#     col1, col2 = st.columns([3, 1])
    
#     with col1:
#         # Chat container
#         chat_container = st.container()
#         with chat_container:
#             for message in st.session_state.chat_history:
#                 display_chat_message(message['role'], message['content'], message.get('timestamp'))
        
#         # Input area
#         st.markdown("---")
#         user_input = st.text_area(
#             "💬 Describe your health concern:",
#             placeholder="Type your symptoms, ask about medications, describe health issues...",
#             height=100,
#             key="chat_input"
#         )
        
#         send_col, clear_col = st.columns([4, 1])
#         with send_col:
#             if st.button("📤 Send Message", use_container_width=True):
#                 if user_input.strip():
#                     # Add user message to history
#                     user_msg = {
#                         "role": "user", 
#                         "content": user_input,
#                         "timestamp": datetime.now().isoformat()
#                     }
#                     st.session_state.chat_history.append(user_msg)
                    
#                     # Get AI response
#                     with st.spinner("🔍 Analyzing your query..."):
#                         response = api_client.send_chat_message(
#                             user_input, 
#                             st.session_state.session_id
#                         )
                    
#                     if response:
#                         ai_msg = {
#                             "role": "assistant",
#                             "content": response,
#                             "timestamp": datetime.now().isoformat()
#                         }
#                         st.session_state.chat_history.append(ai_msg)
#                     else:
#                         st.error("❌ Failed to get response from AI assistant")
                    
#                     st.rerun()
        
#         with clear_col:
#             if st.button("🗑️ Clear", use_container_width=True):
#                 st.session_state.chat_history = []
#                 st.rerun()
    
#     with col2:
#         st.markdown("### ⚡ Quick Actions")
        
#         quick_actions = [
#             ("🔍 Symptom Analysis", "Symptom"),
#             ("💊 Drug Check", "Drug"), 
#             ("📚 Medical Terms", "Medical"),
#             ("🚨 Triage", "Triage"),
#             ("📅 Appointment", "Appointment")
#         ]
        
#         for action, page in quick_actions:
#             if st.button(action, use_container_width=True, key=f"quick_{page}"):
#                 st.session_state.current_page = page
#                 st.rerun()
        
#         st.markdown("### 👨‍⚕️ Specialists")
#         specialists = [
#             "Cardiology", "Dermatology", "Neurology", 
#             "Pediatrics", "Mental Health"
#         ]
        
#         for spec in specialists:
#             if st.button(f"👨‍⚕️ {spec}", use_container_width=True, key=f"spec_{spec}"):
#                 st.session_state.current_page = "Specialist"
#                 st.session_state.specialist_type = spec
#                 st.rerun()

# def render_symptom_analyzer():
#     """Render symptom analysis interface"""
#     st.markdown('<div class="main-header">🔍 Symptom Analyzer</div>', unsafe_allow_html=True)
    
#     with st.form("symptom_form"):
#         symptoms = st.text_area(
#             "Describe your symptoms in detail:",
#             placeholder="Example: headache, fever for 2 days, nausea, dizziness...",
#             help="Be specific about each symptom and their characteristics"
#         )
        
#         col1, col2 = st.columns(2)
#         with col1:
#             duration = st.selectbox(
#                 "🕒 Duration:",
#                 ["not specified", "less than 24 hours", "1-3 days", "3-7 days", "1-2 weeks", "more than 2 weeks"]
#             )
#         with col2:
#             severity = st.selectbox(
#                 "📊 Severity:",
#                 ["not specified", "mild", "moderate", "severe", "very severe"]
#             )
        
#         if st.form_submit_button("🔍 Analyze Symptoms"):
#             if symptoms.strip():
#                 with st.spinner("Analyzing your symptoms..."):
#                     symptom_list = [s.strip() for s in symptoms.split(",") if s.strip()]
#                     result = api_client.analyze_symptoms(symptom_list, duration, severity)
                
#                 if result:
#                     display_analysis_result(result, "Symptom Analysis")
#                 else:
#                     st.error("❌ Failed to analyze symptoms")
#             else:
#                 st.warning("⚠️ Please describe your symptoms")

# def render_drug_checker():
#     """Render drug interaction checker"""
#     st.markdown('<div class="main-header">💊 Drug Interaction Checker</div>', unsafe_allow_html=True)
    
#     with st.form("drug_form"):
#         medications = st.text_area(
#             "💊 Medications you're taking:",
#             placeholder="Example: aspirin, metformin, vitamin D, lisinopril...",
#             help="List all medications, supplements, and vitamins"
#         )
        
#         col1, col2 = st.columns(2)
#         with col1:
#             age = st.number_input("👤 Age", min_value=0, max_value=120, value=0)
#             conditions = st.text_input("🏥 Existing conditions")
#         with col2:
#             gender = st.selectbox("⚧ Gender", ["not specified", "male", "female", "other"])
#             other_meds = st.text_input("💊 Other medications/supplements")
        
#         if st.form_submit_button("🔍 Check Interactions"):
#             if medications.strip():
#                 with st.spinner("Checking drug interactions..."):
#                     med_list = [m.strip() for m in medications.split(",") if m.strip()]
#                     condition_list = [c.strip() for c in conditions.split(",")] if conditions else []
#                     other_med_list = [m.strip() for m in other_meds.split(",")] if other_meds else []
                    
#                     result = api_client.check_drug_interactions(
#                         med_list, age if age > 0 else None,
#                         gender if gender != "not specified" else None,
#                         condition_list, other_med_list
#                     )
                
#                 if result:
#                     display_analysis_result(result, "Drug Interaction Analysis")
#                 else:
#                     st.error("❌ Failed to check drug interactions")
#             else:
#                 st.warning("⚠️ Please enter at least one medication")

# def render_medical_terms():
#     """Render medical term explorer"""
#     st.markdown('<div class="main-header">📚 Medical Term Explorer</div>', unsafe_allow_html=True)
    
#     with st.form("term_form"):
#         term = st.text_input(
#             "Enter medical term:",
#             placeholder="Example: hypertension, myocardial infarction, diabetes..."
#         )
        
#         language = st.selectbox("🌐 Language", ["en", "hi", "es", "fr", "de"])
        
#         if st.form_submit_button("🔍 Explain Term"):
#             if term.strip():
#                 with st.spinner("Getting explanation..."):
#                     result = api_client.explain_medical_term(term, language)
                
#                 if result:
#                     display_analysis_result(result, "Medical Term Explanation")
#                 else:
#                     st.error("❌ Failed to get term explanation")
#             else:
#                 st.warning("⚠️ Please enter a medical term")

# def render_triage():
#     """Render triage assessment"""
#     st.markdown('<div class="main-header">🚨 Triage Assessment</div>', unsafe_allow_html=True)
    
#     with st.form("triage_form"):
#         st.subheader("Chief Complaint")
#         chief_complaint = st.text_input("Primary reason for seeking care:")
        
#         st.subheader("Symptoms")
#         symptoms = st.text_area("List all current symptoms (comma separated):")
        
#         col1, col2 = st.columns(2)
#         with col1:
#             duration = st.selectbox("Duration:", ["not specified", "<24 hours", "1-3 days", "3-7 days", "1-2 weeks", ">2 weeks"])
#             severity = st.selectbox("Severity:", ["not specified", "mild", "moderate", "severe", "very severe"])
#             age = st.number_input("Age", min_value=0, max_value=120, value=0)
        
#         with col2:
#             pain_level = st.slider("Pain level (0-10)", 0, 10, 0)
#             gender = st.selectbox("Gender", ["not specified", "male", "female", "other"])
#             medical_history = st.text_input("Medical history")
        
#         if st.form_submit_button("🚨 Assess Urgency"):
#             if chief_complaint.strip() and symptoms.strip():
#                 triage_data = {
#                     "chief_complaint": chief_complaint,
#                     "symptoms": [s.strip() for s in symptoms.split(",") if s.strip()],
#                     "duration": duration,
#                     "severity": severity,
#                     "age": age if age > 0 else None,
#                     "gender": gender if gender != "not specified" else None,
#                     "pain_level": pain_level if pain_level > 0 else None,
#                     "medical_history": [m.strip() for m in medical_history.split(",")] if medical_history else []
#                 }
                
#                 with st.spinner("Performing triage assessment..."):
#                     result = api_client.triage_assessment(triage_data)
                
#                 if result:
#                     display_analysis_result(result, "Triage Assessment")
#                 else:
#                     st.error("❌ Failed to perform triage assessment")
#             else:
#                 st.warning("⚠️ Please fill in chief complaint and symptoms")

# def render_appointment():
#     """Render appointment booking"""
#     st.markdown('<div class="main-header">📅 Book Appointment</div>', unsafe_allow_html=True)
    
#     with st.form("appointment_form"):
#         col1, col2 = st.columns(2)
#         with col1:
#             name = st.text_input("👤 Full Name:")
#             service = st.selectbox("🏥 Service:", ["General Consultation", "Specialist", "Follow-up", "Emergency", "Checkup"])
#         with col2:
#             contact = st.text_input("📞 Contact:")
#             preferred_date = st.date_input("📅 Preferred Date:")
        
#         symptoms = st.text_area("💬 Reason for appointment:")
        
#         if st.form_submit_button("📅 Book Appointment"):
#             if name and contact:
#                 with st.spinner("Booking appointment..."):
#                     result = api_client.book_appointment(name, service, contact)
                
#                 if result and result.get('success'):
#                     st.success("✅ Appointment booked successfully!")
#                     st.json(result)
#                 else:
#                     st.error("❌ Failed to book appointment")
#             else:
#                 st.warning("⚠️ Please fill in name and contact details")

# def render_specialist():
#     """Render specialist consultation"""
#     specialist = st.session_state.specialist_type
#     st.markdown(f'<div class="main-header">👨‍⚕️ {specialist} Consultation</div>', unsafe_allow_html=True)
    
#     query = st.text_area(
#         f"Describe your {specialist.lower()} concerns:",
#         height=150,
#         placeholder=f"Example: I'm experiencing symptoms related to {specialist.lower()} such as..."
#     )
    
#     if st.button(f"👨‍⚕️ Consult {specialist}"):
#         if query.strip():
#             with st.spinner(f"Consulting {specialist} specialist..."):
#                 result = api_client.consult_specialist(
#                     specialist.lower(), 
#                     query, 
#                     st.session_state.session_id
#                 )
            
#             if result:
#                 display_analysis_result(result, f"{specialist} Consultation")
#             else:
#                 st.error(f"❌ Failed to consult {specialist} specialist")
#         else:
#             st.warning("⚠️ Please describe your concerns")

# def display_analysis_result(result: Dict, title: str):
#     """Display analysis result in a structured format"""
#     st.markdown(f'<div class="card success-card"><h3>✅ {title} Complete</h3></div>', unsafe_allow_html=True)
    
#     # Summary
#     if 'summary' in result:
#         st.subheader("📋 Summary")
#         st.write(result['summary'])
    
#     # Detailed analysis
#     if 'detailed_analysis' in result and result['detailed_analysis']:
#         with st.expander("📖 Detailed Analysis"):
#             st.write(result['detailed_analysis'])
    
#     # Recommendations
#     if 'recommendations' in result and result['recommendations']:
#         st.subheader("💡 Recommendations")
#         for i, rec in enumerate(result['recommendations'], 1):
#             st.write(f"{i}. {rec}")
    
#     # When to seek help
#     if 'when_to_seek_help' in result and result['when_to_seek_help']:
#         st.subheader("🚨 When to Seek Help")
#         for i, when in enumerate(result['when_to_seek_help'], 1):
#             st.write(f"{i}. {when}")
    
#     # Triage information
#     if 'triage_level' in result:
#         st.subheader("⚠️ Triage Level")
#         st.error(f"**{result['triage_level'].upper()}**")
    
#     # Additional fields
#     additional_fields = ['key_findings', 'next_steps', 'emergency_signs']
#     for field in additional_fields:
#         if field in result and result[field]:
#             st.subheader(f"📊 {field.replace('_', ' ').title()}")
#             for i, item in enumerate(result[field], 1):
#                 st.write(f"{i}. {item}")

# def main():
#     """Main application function"""
#     initialize_session_state()
    
#     # Sidebar navigation
#     st.sidebar.markdown('<div class="main-header">🏥 Medicura AI</div>', unsafe_allow_html=True)
    
#     # Test connection button
#     if st.sidebar.button("🔗 Test Connection"):
#         if test_api_connection():
#             st.sidebar.success("✅ Backend connected!")
#         else:
#             st.sidebar.error("❌ Backend connection failed")
    
#     # Navigation
#     st.sidebar.markdown("### 🧭 Navigation")
#     pages = {
#         "Dashboard": "🏠 Dashboard",
#         "Chatbot": "🤖 AI Chatbot", 
#         "Symptom": "🔍 Symptom Analysis",
#         "Drug": "💊 Drug Checker",
#         "Medical": "📚 Medical Terms",
#         "Triage": "🚨 Triage",
#         "Appointment": "📅 Appointment",
#         "Specialist": "👨‍⚕️ Specialist"
#     }
    
#     selected_page = st.sidebar.radio("Go to", list(pages.keys()), 
#                                    format_func=lambda x: pages[x])
    
#     st.session_state.current_page = selected_page
    
#     # Session info
#     st.sidebar.markdown("---")
#     st.sidebar.markdown("### 💾 Session Info")
#     st.sidebar.write(f"ID: `{st.session_state.session_id[:8]}...`")
#     st.sidebar.write(f"Messages: {len(st.session_state.chat_history)}")
    
#     if st.sidebar.button("🆕 New Session"):
#         st.session_state.session_id = str(uuid.uuid4())
#         st.session_state.chat_history = []
#         st.sidebar.success("New session started!")
#         st.rerun()
    
#     # Disclaimer
#     st.sidebar.markdown("---")
#     st.sidebar.markdown("""
#     ### ⚠️ Disclaimer
#     This AI assistant provides general health information and is not a substitute for professional medical advice.
#     """)
    
#     # Render selected page
#     if st.session_state.current_page == "Dashboard":
#         render_dashboard()
#     elif st.session_state.current_page == "Chatbot":
#         render_chatbot()
#     elif st.session_state.current_page == "Symptom":
#         render_symptom_analyzer()
#     elif st.session_state.current_page == "Drug":
#         render_drug_checker()
#     elif st.session_state.current_page == "Medical":
#         render_medical_terms()
#     elif st.session_state.current_page == "Triage":
#         render_triage()
#     elif st.session_state.current_page == "Appointment":
#         render_appointment()
#     elif st.session_state.current_page == "Specialist":
#         render_specialist()

# if __name__ == "__main__":
#     main()


import streamlit as st
import requests
import json
import uuid
from datetime import datetime, timedelta
import pandas as pd
import time
import os
from typing import List, Dict, Any, Optional

# Page configuration
st.set_page_config(
    page_title="Medicura AI Health Assistant",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional medical UI
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #2563eb;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: bold;
    }
    .sub-header {
        font-size: 1.4rem;
        color: #dc2626;
        margin-bottom: 1rem;
        font-weight: 600;
    }
    .card {
        background-color: #f8fafc;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #2563eb;
        margin: 10px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .emergency-card {
        background-color: #fef2f2;
        border-left: 5px solid #dc2626;
    }
    .success-card {
        background-color: #f0fdf4;
        border-left: 5px solid #16a34a;
    }
    .chat-user {
        background: linear-gradient(135deg, #2563eb, #1d4ed8);
        color: white;
        padding: 12px 16px;
        border-radius: 15px 15px 5px 15px;
        margin: 8px 0;
        max-width: 80%;
        margin-left: auto;
    }
    .chat-assistant {
        background: linear-gradient(135deg, #f3f4f6, #e5e7eb);
        color: #1f2937;
        padding: 12px 16px;
        border-radius: 15px 15px 15px 5px;
        margin: 8px 0;
        max-width: 80%;
        margin-right: auto;
        border: 1px solid #d1d5db;
    }
    .reminder-card {
        background: linear-gradient(135deg, #fff7ed, #ffedd5);
        border-left: 5px solid #f97316;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Backend API configuration - Replace with your actual backend URL
BACKEND_URL = "https://hg-medicura-ai-backend-production.up.railway.app"

class MedicuraAPIClient:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.timeout = 30
    
    def _make_request(self, endpoint: str, payload: Dict = None, method: str = "POST"):
        """Generic request handler"""
        url = f"{self.base_url}{endpoint}"
        try:
            if method == "POST":
                response = requests.post(url, json=payload, timeout=self.timeout)
            else:
                response = requests.get(url, params=payload, timeout=self.timeout)
            
            if response.status_code == 200:
                return response.json()
            else:
                st.error(f"API Error: Status {response.status_code} for {endpoint}")
                return None
        except Exception as e:
            st.error(f"Connection Error: {str(e)}")
            return None
    
    # Chatbot endpoints
    def send_chat_message(self, message: str, session_id: str = None) -> Optional[Dict]:
        """Send message to main chatbot"""
        endpoint = "/api/chatbot"
        payload = {"message": message, "session_id": session_id}
        return self._make_request(endpoint, payload)
    
    def clear_session(self, session_id: str) -> bool:
        """Clear chat session"""
        endpoint = "/api/chatbot/session/clear"
        payload = {"session_id": session_id}
        result = self._make_request(endpoint, payload)
        return result is not None
    
    # Health endpoints - FIXED ENDPOINTS
    def analyze_symptoms(self, symptoms: List[str], duration: str = None, severity: str = None) -> Optional[Dict]:
        """Analyze symptoms"""
        endpoint = "/api/health/symptom-analyzer"
        payload = {
            "symptoms": symptoms,
            "duration": duration or "not specified",
            "severity": severity or "not specified"
        }
        return self._make_request(endpoint, payload)
    
    def check_drug_interactions(self, medications: List[str], age: int = None, 
                               gender: str = None, conditions: List[str] = None, 
                               other_meds: List[str] = None) -> Optional[Dict]:
        """Check drug interactions"""
        endpoint = "/api/health/drug-interactions"
        payload = {
            "medications": medications,
            "age": age,
            "gender": gender,
            "existing_conditions": conditions or [],
            "other_medications": other_meds or []
        }
        return self._make_request(endpoint, payload)
    
    def explain_medical_term(self, term: str, language: str = "en") -> Optional[Dict]:
        """Explain medical term"""
        endpoint = "/api/health/medical-term"
        payload = {"term": term, "language": language}
        return self._make_request(endpoint, payload)
    
    def triage_assessment(self, triage_data: Dict) -> Optional[Dict]:
        """Perform triage assessment - FIXED ENDPOINT"""
        endpoint = "/api/health/triage"
        return self._make_request(endpoint, triage_data)
    
    def summarize_report(self, text: str, language: str = "en") -> Optional[Dict]:
        """Summarize medical report"""
        endpoint = "/api/health/report-summarize"
        payload = {"text": text, "language": language}
        return self._make_request(endpoint, payload)
    
    # Booking endpoint - FIXED ENDPOINT
    def book_appointment(self, name: str, service: str, contact: str) -> Optional[Dict]:
        """Book appointment"""
        endpoint = "/book"
        # Using params instead of JSON for GET-style endpoint
        payload = {
            "citizen_name": name,
            "service": service,
            "contact": contact
        }
        return self._make_request(endpoint, payload, method="POST")
    
    # Specialist consultation - FIXED ENDPOINT
    def consult_specialist(self, specialist_type: str, query: str, session_id: str = None) -> Optional[Dict]:
        """Consult with specialist"""
        endpoint = "/api/specialist/consult"
        payload = {
            "specialist_type": specialist_type,
            "query": query,
            "session_id": session_id
        }
        return self._make_request(endpoint, payload)
    
    # Test endpoints
    def test_connection(self) -> bool:
        """Test backend connection"""
        endpoint = "/health"
        result = self._make_request(endpoint, method="GET")
        return result is not None and result.get("status") == "healthy"

# Initialize API client
api_client = MedicuraAPIClient(BACKEND_URL)

# Medicine Reminder System
class MedicineReminder:
    def __init__(self):
        if 'reminders' not in st.session_state:
            st.session_state.reminders = []
    
    def add_reminder(self, medicine_name: str, dosage: str, frequency: str, 
                    start_date: datetime, duration_days: int, notes: str = ""):
        """Add a new medicine reminder"""
        reminder = {
            'id': str(uuid.uuid4()),
            'medicine_name': medicine_name,
            'dosage': dosage,
            'frequency': frequency,
            'start_date': start_date,
            'end_date': start_date + timedelta(days=duration_days),
            'notes': notes,
            'created_at': datetime.now(),
            'active': True
        }
        st.session_state.reminders.append(reminder)
        return reminder
    
    def get_active_reminders(self):
        """Get active reminders"""
        now = datetime.now()
        active_reminders = []
        for reminder in st.session_state.reminders:
            if (reminder['active'] and 
                reminder['start_date'] <= now <= reminder['end_date']):
                active_reminders.append(reminder)
        return active_reminders
    
    def delete_reminder(self, reminder_id: str):
        """Delete a reminder"""
        st.session_state.reminders = [
            r for r in st.session_state.reminders if r['id'] != reminder_id
        ]
    
    def toggle_reminder(self, reminder_id: str):
        """Toggle reminder active status"""
        for reminder in st.session_state.reminders:
            if reminder['id'] == reminder_id:
                reminder['active'] = not reminder['active']
                break

# Initialize reminder system
reminder_system = MedicineReminder()

def initialize_session_state():
    """Initialize all session state variables"""
    if 'session_id' not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "Dashboard"
    if 'specialist_type' not in st.session_state:
        st.session_state.specialist_type = "General"
    if 'api_connected' not in st.session_state:
        st.session_state.api_connected = False

def test_api_connection():
    """Test connection to backend API"""
    with st.spinner("Testing connection to Medicura AI Backend..."):
        if api_client.test_connection():
            st.session_state.api_connected = True
            return True
        else:
            st.session_state.api_connected = False
            return False

def display_chat_message(role: str, content: Any, timestamp: str = None):
    """Display chat message with appropriate styling"""
    if role == "user":
        st.markdown(f"""
        <div class="chat-user">
            <strong>You:</strong> {content}<br>
            <small>{timestamp if timestamp else datetime.now().strftime('%H:%M')}</small>
        </div>
        """, unsafe_allow_html=True)
    else:
        try:
            # Try to parse JSON response
            if isinstance(content, str):
                try:
                    response_data = json.loads(content)
                except:
                    response_data = {"summary": content}
            else:
                response_data = content
            
            summary = response_data.get('summary', 'No summary available')
            
            st.markdown(f"""
            <div class="chat-assistant">
                <strong>Medicura AI:</strong> {summary}<br>
                <small>{timestamp if timestamp else datetime.now().strftime('%H:%M')}</small>
            </div>
            """, unsafe_allow_html=True)
            
            # Display additional information if available
            additional_fields = [
                ('detailed_analysis', '📖 Detailed Analysis'),
                ('recommendations', '💡 Recommendations'),
                ('when_to_seek_help', '🚨 When to Seek Help'),
                ('key_findings', '🔍 Key Findings')
            ]
            
            has_additional_content = any(
                response_data.get(field) and response_data[field] != summary 
                for field, _ in additional_fields
            )
            
            if has_additional_content:
                with st.expander("View Details", expanded=False):
                    for field, title in additional_fields:
                        if response_data.get(field) and response_data[field] != summary:
                            st.markdown(f"**{title}:**")
                            if isinstance(response_data[field], list):
                                for i, item in enumerate(response_data[field], 1):
                                    st.write(f"{i}. {item}")
                            else:
                                st.write(response_data[field])
                            st.markdown("---")
                        
        except Exception as e:
            st.markdown(f"""
            <div class="chat-assistant">
                <strong>Medicura AI:</strong> {content}<br>
                <small>{timestamp if timestamp else datetime.now().strftime('%H:%M')}</small>
            </div>
            """, unsafe_allow_html=True)

def render_dashboard():
    """Render main dashboard"""
    st.markdown('<div class="main-header">🏥 Medicura AI Health Assistant</div>', unsafe_allow_html=True)
    
    # Connection status
    col1, col2, col3 = st.columns([2, 1, 1])
    with col2:
        status_color = "🟢" if st.session_state.api_connected else "🔴"
        st.write(f"{status_color} Backend: {'Connected' if st.session_state.api_connected else 'Disconnected'}")
    
    # Emergency banner
    st.markdown("""
    <div class="card emergency-card">
        <h3>🚨 Emergency Notice</h3>
        <p>If you are experiencing a medical emergency, please call your local emergency number immediately. 
        This AI assistant is for informational purposes only and cannot provide emergency medical care.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Feature cards
    st.markdown("### 🚀 Quick Access Features")
    
    cols = st.columns(4)
    features = [
        ("🤖 AI Chatbot", "General health conversations"),
        ("🔍 Symptom Check", "Analyze your symptoms"), 
        ("💊 Drug Check", "Medication interactions"),
        ("⏰ Medicine Reminder", "Set medication alerts")
    ]
    
    for i, (title, desc) in enumerate(features):
        with cols[i]:
            if st.button(f"**{title}**\n\n{desc}", use_container_width=True, key=f"feature_{i}"):
                page_map = {
                    "AI Chatbot": "Chatbot",
                    "Symptom Check": "Symptom",
                    "Drug Check": "Drug", 
                    "Medicine Reminder": "Reminders"
                }
                st.session_state.current_page = page_map.get(title, "Dashboard")
                st.rerun()
    
    # Active reminders preview
    active_reminders = reminder_system.get_active_reminders()
    if active_reminders:
        st.markdown("### ⏰ Active Reminders")
        for reminder in active_reminders[:3]:  # Show max 3
            days_left = (reminder['end_date'] - datetime.now()).days
            st.markdown(f"""
            <div class="reminder-card">
                <strong>💊 {reminder['medicine_name']}</strong><br>
                Dosage: {reminder['dosage']} | Frequency: {reminder['frequency']}<br>
                <small>⏳ {days_left} days remaining</small>
            </div>
            """, unsafe_allow_html=True)
    
    # Recent chat preview
    if st.session_state.chat_history:
        st.markdown("### 💬 Recent Conversation")
        recent_messages = st.session_state.chat_history[-3:]  # Last 3 messages
        for msg in recent_messages:
            display_chat_message(msg['role'], msg['content'], msg.get('timestamp'))

def render_chatbot():
    """Render AI chatbot interface"""
    st.markdown('<div class="main-header">🤖 Medicura AI Chatbot</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Chat container
        chat_container = st.container()
        with chat_container:
            for message in st.session_state.chat_history:
                display_chat_message(message['role'], message['content'], message.get('timestamp'))
        
        # Input area
        st.markdown("---")
        user_input = st.text_area(
            "💬 Describe your health concern:",
            placeholder="Type your symptoms, ask about medications, describe health issues...",
            height=100,
            key="chat_input"
        )
        
        send_col, clear_col = st.columns([4, 1])
        with send_col:
            if st.button("📤 Send Message", use_container_width=True):
                if user_input.strip():
                    # Add user message to history
                    user_msg = {
                        "role": "user", 
                        "content": user_input,
                        "timestamp": datetime.now().isoformat()
                    }
                    st.session_state.chat_history.append(user_msg)
                    
                    # Get AI response
                    with st.spinner("🔍 Analyzing your query..."):
                        response = api_client.send_chat_message(
                            user_input, 
                            st.session_state.session_id
                        )
                    
                    if response:
                        ai_msg = {
                            "role": "assistant",
                            "content": response,
                            "timestamp": datetime.now().isoformat()
                        }
                        st.session_state.chat_history.append(ai_msg)
                    else:
                        st.error("❌ Failed to get response from AI assistant")
                    
                    st.rerun()
        
        with clear_col:
            if st.button("🗑️ Clear", use_container_width=True):
                st.session_state.chat_history = []
                st.rerun()
    
    with col2:
        st.markdown("### ⚡ Quick Actions")
        
        quick_actions = [
            ("🔍 Symptom Analysis", "Symptom"),
            ("💊 Drug Check", "Drug"), 
            ("📚 Medical Terms", "Medical"),
            ("🚨 Triage", "Triage"),
            ("📅 Appointment", "Appointment"),
            ("⏰ Reminders", "Reminders")
        ]
        
        for action, page in quick_actions:
            if st.button(action, use_container_width=True, key=f"quick_{page}"):
                st.session_state.current_page = page
                st.rerun()
        
        st.markdown("### 👨‍⚕️ Specialists")
        specialists = [
            "Cardiology", "Dermatology", "Neurology", 
            "Pediatrics", "Mental Health"
        ]
        
        for spec in specialists:
            if st.button(f"👨‍⚕️ {spec}", use_container_width=True, key=f"spec_{spec}"):
                st.session_state.current_page = "Specialist"
                st.session_state.specialist_type = spec
                st.rerun()

def render_symptom_analyzer():
    """Render symptom analysis interface"""
    st.markdown('<div class="main-header">🔍 Symptom Analyzer</div>', unsafe_allow_html=True)
    
    with st.form("symptom_form"):
        symptoms = st.text_area(
            "Describe your symptoms in detail:",
            placeholder="Example: headache, fever for 2 days, nausea, dizziness...",
            help="Be specific about each symptom and their characteristics"
        )
        
        col1, col2 = st.columns(2)
        with col1:
            duration = st.selectbox(
                "🕒 Duration:",
                ["not specified", "less than 24 hours", "1-3 days", "3-7 days", "1-2 weeks", "more than 2 weeks"]
            )
        with col2:
            severity = st.selectbox(
                "📊 Severity:",
                ["not specified", "mild", "moderate", "severe", "very severe"]
            )
        
        if st.form_submit_button("🔍 Analyze Symptoms"):
            if symptoms.strip():
                with st.spinner("Analyzing your symptoms..."):
                    symptom_list = [s.strip() for s in symptoms.split(",") if s.strip()]
                    result = api_client.analyze_symptoms(symptom_list, duration, severity)
                
                if result:
                    display_analysis_result(result, "Symptom Analysis")
                else:
                    st.error("❌ Failed to analyze symptoms")
            else:
                st.warning("⚠️ Please describe your symptoms")

def render_drug_checker():
    """Render drug interaction checker"""
    st.markdown('<div class="main-header">💊 Drug Interaction Checker</div>', unsafe_allow_html=True)
    
    with st.form("drug_form"):
        medications = st.text_area(
            "💊 Medications you're taking:",
            placeholder="Example: aspirin, metformin, vitamin D, lisinopril...",
            help="List all medications, supplements, and vitamins"
        )
        
        col1, col2 = st.columns(2)
        with col1:
            age = st.number_input("👤 Age", min_value=0, max_value=120, value=0)
            conditions = st.text_input("🏥 Existing conditions")
        with col2:
            gender = st.selectbox("⚧ Gender", ["not specified", "male", "female", "other"])
            other_meds = st.text_input("💊 Other medications/supplements")
        
        if st.form_submit_button("🔍 Check Interactions"):
            if medications.strip():
                with st.spinner("Checking drug interactions..."):
                    med_list = [m.strip() for m in medications.split(",") if m.strip()]
                    condition_list = [c.strip() for c in conditions.split(",")] if conditions else []
                    other_med_list = [m.strip() for m in other_meds.split(",")] if other_meds else []
                    
                    result = api_client.check_drug_interactions(
                        med_list, age if age > 0 else None,
                        gender if gender != "not specified" else None,
                        condition_list, other_med_list
                    )
                
                if result:
                    display_analysis_result(result, "Drug Interaction Analysis")
                else:
                    st.error("❌ Failed to check drug interactions")
            else:
                st.warning("⚠️ Please enter at least one medication")

def render_medical_terms():
    """Render medical term explorer"""
    st.markdown('<div class="main-header">📚 Medical Term Explorer</div>', unsafe_allow_html=True)
    
    with st.form("term_form"):
        term = st.text_input(
            "Enter medical term:",
            placeholder="Example: hypertension, myocardial infarction, diabetes..."
        )
        
        language = st.selectbox("🌐 Language", ["en", "hi", "es", "fr", "de"])
        
        if st.form_submit_button("🔍 Explain Term"):
            if term.strip():
                with st.spinner("Getting explanation..."):
                    result = api_client.explain_medical_term(term, language)
                
                if result:
                    display_analysis_result(result, "Medical Term Explanation")
                else:
                    st.error("❌ Failed to get term explanation")
            else:
                st.warning("⚠️ Please enter a medical term")

def render_triage():
    """Render triage assessment"""
    st.markdown('<div class="main-header">🚨 Triage Assessment</div>', unsafe_allow_html=True)
    
    with st.form("triage_form"):
        st.subheader("Chief Complaint")
        chief_complaint = st.text_input("Primary reason for seeking care:")
        
        st.subheader("Symptoms")
        symptoms = st.text_area("List all current symptoms (comma separated):")
        
        col1, col2 = st.columns(2)
        with col1:
            duration = st.selectbox("Duration:", ["not specified", "<24 hours", "1-3 days", "3-7 days", "1-2 weeks", ">2 weeks"])
            severity = st.selectbox("Severity:", ["not specified", "mild", "moderate", "severe", "very severe"])
            age = st.number_input("Age", min_value=0, max_value=120, value=0)
        
        with col2:
            pain_level = st.slider("Pain level (0-10)", 0, 10, 0)
            gender = st.selectbox("Gender", ["not specified", "male", "female", "other"])
            medical_history = st.text_input("Medical history")
        
        if st.form_submit_button("🚨 Assess Urgency"):
            if chief_complaint.strip() and symptoms.strip():
                triage_data = {
                    "chief_complaint": chief_complaint,
                    "symptoms": [s.strip() for s in symptoms.split(",") if s.strip()],
                    "duration": duration,
                    "severity": severity,
                    "age": age if age > 0 else None,
                    "gender": gender if gender != "not specified" else None,
                    "pain_level": pain_level if pain_level > 0 else None,
                    "medical_history": [m.strip() for m in medical_history.split(",")] if medical_history else []
                }
                
                with st.spinner("Performing triage assessment..."):
                    result = api_client.triage_assessment(triage_data)
                
                if result:
                    display_analysis_result(result, "Triage Assessment")
                else:
                    st.error("❌ Failed to perform triage assessment")
            else:
                st.warning("⚠️ Please fill in chief complaint and symptoms")

def render_appointment():
    """Render appointment booking"""
    st.markdown('<div class="main-header">📅 Book Appointment</div>', unsafe_allow_html=True)
    
    with st.form("appointment_form"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("👤 Full Name:")
            service = st.selectbox("🏥 Service:", ["General Consultation", "Specialist", "Follow-up", "Emergency", "Checkup"])
        with col2:
            contact = st.text_input("📞 Contact:")
            preferred_date = st.date_input("📅 Preferred Date:")
        
        symptoms = st.text_area("💬 Reason for appointment:")
        
        if st.form_submit_button("📅 Book Appointment"):
            if name and contact:
                with st.spinner("Booking appointment..."):
                    result = api_client.book_appointment(name, service, contact)
                
                if result and result.get('success'):
                    st.success("✅ Appointment booked successfully!")
                    st.json(result)
                else:
                    st.error("❌ Failed to book appointment")
            else:
                st.warning("⚠️ Please fill in name and contact details")

def render_specialist():
    """Render specialist consultation"""
    specialist = st.session_state.specialist_type
    st.markdown(f'<div class="main-header">👨‍⚕️ {specialist} Consultation</div>', unsafe_allow_html=True)
    
    query = st.text_area(
        f"Describe your {specialist.lower()} concerns:",
        height=150,
        placeholder=f"Example: I'm experiencing symptoms related to {specialist.lower()} such as..."
    )
    
    if st.button(f"👨‍⚕️ Consult {specialist}"):
        if query.strip():
            with st.spinner(f"Consulting {specialist} specialist..."):
                result = api_client.consult_specialist(
                    specialist.lower(), 
                    query, 
                    st.session_state.session_id
                )
            
            if result:
                display_analysis_result(result, f"{specialist} Consultation")
            else:
                st.error(f"❌ Failed to consult {specialist} specialist")
        else:
            st.warning("⚠️ Please describe your concerns")

def render_reminders():
    """Render medicine reminder interface"""
    st.markdown('<div class="main-header">⏰ Medicine Reminder</div>', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["➕ Add New Reminder", "📋 Active Reminders"])
    
    with tab1:
        st.subheader("Add Medicine Reminder")
        with st.form("reminder_form"):
            col1, col2 = st.columns(2)
            with col1:
                medicine_name = st.text_input("💊 Medicine Name:")
                dosage = st.text_input("📏 Dosage (e.g., 500mg, 1 tablet):")
            with col2:
                frequency = st.selectbox("🕒 Frequency:", 
                    ["Once daily", "Twice daily", "Three times daily", 
                     "Every 6 hours", "Every 8 hours", "Weekly", "As needed"])
                duration_days = st.number_input("📅 Duration (days):", min_value=1, max_value=365, value=7)
            
            start_date = st.date_input("📅 Start Date:", value=datetime.now())
            notes = st.text_area("📝 Notes (optional):")
            
            if st.form_submit_button("💾 Save Reminder"):
                if medicine_name and dosage:
                    reminder = reminder_system.add_reminder(
                        medicine_name, dosage, frequency, 
                        datetime.combine(start_date, datetime.now().time()),
                        duration_days, notes
                    )
                    st.success(f"✅ Reminder set for {medicine_name}!")
                else:
                    st.warning("⚠️ Please fill in medicine name and dosage")
    
    with tab2:
        st.subheader("Active Reminders")
        active_reminders = reminder_system.get_active_reminders()
        
        if not active_reminders:
            st.info("No active reminders. Add a new reminder above.")
        else:
            for reminder in active_reminders:
                days_left = (reminder['end_date'] - datetime.now()).days
                col1, col2, col3 = st.columns([3, 1, 1])
                
                with col1:
                    st.markdown(f"""
                    <div class="reminder-card">
                        <strong>💊 {reminder['medicine_name']}</strong><br>
                        <strong>Dosage:</strong> {reminder['dosage']}<br>
                        <strong>Frequency:</strong> {reminder['frequency']}<br>
                        <strong>Duration:</strong> {days_left} days remaining<br>
                        <strong>Notes:</strong> {reminder['notes'] or 'None'}
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    if st.button("❌ Delete", key=f"del_{reminder['id']}"):
                        reminder_system.delete_reminder(reminder['id'])
                        st.rerun()
                
                with col3:
                    status = "🟢 Active" if reminder['active'] else "🔴 Inactive"
                    if st.button(status, key=f"toggle_{reminder['id']}"):
                        reminder_system.toggle_reminder(reminder['id'])
                        st.rerun()

def display_analysis_result(result: Dict, title: str):
    """Display analysis result in a structured format"""
    st.markdown(f'<div class="card success-card"><h3>✅ {title} Complete</h3></div>', unsafe_allow_html=True)
    
    # Summary
    if 'summary' in result:
        st.subheader("📋 Summary")
        st.write(result['summary'])
    
    # Detailed analysis
    if 'detailed_analysis' in result and result['detailed_analysis']:
        with st.expander("📖 Detailed Analysis"):
            st.write(result['detailed_analysis'])
    
    # Recommendations
    if 'recommendations' in result and result['recommendations']:
        st.subheader("💡 Recommendations")
        for i, rec in enumerate(result['recommendations'], 1):
            st.write(f"{i}. {rec}")
    
    # When to seek help
    if 'when_to_seek_help' in result and result['when_to_seek_help']:
        st.subheader("🚨 When to Seek Help")
        for i, when in enumerate(result['when_to_seek_help'], 1):
            st.write(f"{i}. {when}")
    
    # Triage information
    if 'triage_level' in result:
        st.subheader("⚠️ Triage Level")
        urgency_color = {
            'Emergency': 'red',
            'Urgent': 'orange', 
            'Semi-Urgent': 'yellow',
            'Non-Urgent': 'green'
        }.get(result['triage_level'], 'gray')
        st.markdown(f"<h3 style='color: {urgency_color};'>{result['triage_level'].upper()}</h3>", unsafe_allow_html=True)
    
    # Additional fields
    additional_fields = ['key_findings', 'next_steps', 'emergency_signs']
    for field in additional_fields:
        if field in result and result[field]:
            st.subheader(f"📊 {field.replace('_', ' ').title()}")
            for i, item in enumerate(result[field], 1):
                st.write(f"{i}. {item}")

def main():
    """Main application function"""
    initialize_session_state()
    
    # Sidebar navigation
    st.sidebar.markdown('<div class="main-header">🏥 Medicura AI</div>', unsafe_allow_html=True)
    
    # Test connection button
    if st.sidebar.button("🔗 Test Connection"):
        if test_api_connection():
            st.sidebar.success("✅ Backend connected!")
        else:
            st.sidebar.error("❌ Backend connection failed")
    
    # Navigation
    st.sidebar.markdown("### 🧭 Navigation")
    pages = {
        "Dashboard": "🏠 Dashboard",
        "Chatbot": "🤖 AI Chatbot", 
        "Symptom": "🔍 Symptom Analysis",
        "Drug": "💊 Drug Checker",
        "Medical": "📚 Medical Terms",
        "Triage": "🚨 Triage",
        "Appointment": "📅 Appointment",
        "Specialist": "👨‍⚕️ Specialist",
        "Reminders": "⏰ Medicine Reminder"
    }
    
    selected_page = st.sidebar.radio("Go to", list(pages.keys()), 
                                   format_func=lambda x: pages[x])
    
    st.session_state.current_page = selected_page
    
    # Session info
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 💾 Session Info")
    st.sidebar.write(f"ID: `{st.session_state.session_id[:8]}...`")
    st.sidebar.write(f"Messages: {len(st.session_state.chat_history)}")
    
    if st.sidebar.button("🆕 New Session"):
        st.session_state.session_id = str(uuid.uuid4())
        st.session_state.chat_history = []
        st.sidebar.success("New session started!")
        st.rerun()
    
    # Active reminders count
    active_count = len(reminder_system.get_active_reminders())
    if active_count > 0:
        st.sidebar.markdown(f"### ⏰ Active Reminders: {active_count}")
    
    # Disclaimer
    st.sidebar.markdown("---")
    st.sidebar.markdown("""
    ### ⚠️ Disclaimer
    This AI assistant provides general health information and is not a substitute for professional medical advice.
    """)
    
    # Render selected page
    if st.session_state.current_page == "Dashboard":
        render_dashboard()
    elif st.session_state.current_page == "Chatbot":
        render_chatbot()
    elif st.session_state.current_page == "Symptom":
        render_symptom_analyzer()
    elif st.session_state.current_page == "Drug":
        render_drug_checker()
    elif st.session_state.current_page == "Medical":
        render_medical_terms()
    elif st.session_state.current_page == "Triage":
        render_triage()
    elif st.session_state.current_page == "Appointment":
        render_appointment()
    elif st.session_state.current_page == "Specialist":
        render_specialist()
    elif st.session_state.current_page == "Reminders":
        render_reminders()

if __name__ == "__main__":
    main()