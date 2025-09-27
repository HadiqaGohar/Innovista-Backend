# 🧠 Conversation History Implementation

The Medicura Triage Agent now includes comprehensive conversation history functionality to provide contextual and personalized medical assessments.

## 🎯 Key Features

### 1. **Session-Based Memory**
- Each conversation has a unique `session_id`
- History is stored in TiDB database
- Maintains up to 20 recent messages per session
- Automatic session isolation between different users

### 2. **Contextual Responses**
- Agents remember previous symptoms and conditions
- Build upon previous assessments and recommendations
- Track symptom progression over time
- Provide continuity of care

### 3. **Smart History Integration**
- Last 6 messages (3 exchanges) included in agent context
- Summarized for efficiency while maintaining key information
- Automatic relevance filtering for medical continuity

## 🔄 How It Works

### Chat Flow with History:
```
User: "I have chest pain"
Agent: [Analyzes and provides initial assessment]

User: "The pain is getting worse"
Agent: [References previous chest pain, escalates urgency]

User: "Should I go to ER?"
Agent: [Considers worsening symptoms, provides urgent recommendation]
```

### Database Storage:
```json
{
  "session_id": "user_123",
  "history": [
    {
      "role": "user",
      "content": "I have chest pain",
      "timestamp": "2024-01-15T10:30:00"
    },
    {
      "role": "assistant", 
      "content": "{\"triage_level\": \"HIGH\", \"summary\": \"Chest pain assessment...\"}",
      "timestamp": "2024-01-15T10:30:15"
    }
  ]
}
```

## 📡 API Usage

### 1. **Chat Endpoint with History**
```http
POST /api/chatbot
Content-Type: application/json

{
  "message": "The chest pain is getting worse",
  "session_id": "user_session_123"
}
```

### 2. **Triage Endpoint with History**
```http
POST /api/health/triage
Content-Type: application/json

{
  "chief_complaint": "Worsening chest pain",
  "symptoms": ["chest pain", "nausea", "sweating"],
  "session_id": "user_session_123"
}
```

## 🧪 Testing History Functionality

### Run the Test Script:
```bash
# Start the server first
uvicorn main:app --reload

# In another terminal, run the test
python test_history_functionality.py
```

### Test Scenarios:
1. **Initial Assessment**: Chest pain evaluation
2. **Follow-up**: Worsening symptoms with context
3. **Escalation**: Emergency recommendation based on progression
4. **Session Isolation**: Different sessions don't cross-contaminate

## 💡 Example Conversation

### Initial Contact:
```json
{
  "message": "I have chest pain for 2 hours",
  "session_id": "patient_001"
}
```

**Response:**
```json
{
  "triage_level": "HIGH",
  "urgency_score": 7,
  "case_summary": "45-year-old with chest pain, requires urgent evaluation",
  "routing_decision": "Emergency Department"
}
```

### Follow-up (with history context):
```json
{
  "message": "The pain is now radiating to my arm and I'm sweating",
  "session_id": "patient_001"
}
```

**Response (considers previous chest pain):**
```json
{
  "triage_level": "CRITICAL",
  "urgency_score": 9,
  "case_summary": "Progression of chest pain with cardiac features - possible MI",
  "routing_decision": "Emergency Department",
  "reasoning": "Based on previous chest pain report and new symptoms..."
}
```

## 🔧 Technical Implementation

### History Context in Agent Prompts:
```
USER QUERY: The pain is getting worse
CONTEXT: This is a medical triage assessment.

CONVERSATION HISTORY:
USER: I have chest pain for 2 hours
ASSISTANT: Chest pain assessment - HIGH priority, urgent care needed
USER: The pain is now radiating to my arm
ASSISTANT: Critical escalation - possible cardiac event

Please consider this conversation history when responding...
```

### Database Schema:
```sql
CREATE TABLE chat_sessions (
    session_id VARCHAR(100) PRIMARY KEY,
    history JSON NOT NULL,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

## 🛡️ Privacy & Security

### Data Protection:
- Session IDs are unique and non-guessable
- History automatically expires after inactivity
- No personal identifiers stored in history
- Medical information handled according to privacy standards

### Session Management:
- Automatic cleanup of old sessions
- Session isolation prevents data leakage
- Optional session clearing endpoint available

## 🎯 Benefits

### For Patients:
- **Continuity**: No need to repeat medical history
- **Context**: Agents understand symptom progression
- **Personalization**: Tailored recommendations based on history
- **Efficiency**: Faster, more accurate assessments

### For Healthcare Providers:
- **Documentation**: Complete interaction history
- **Escalation**: Clear progression tracking
- **Quality**: Consistent, context-aware responses
- **Audit Trail**: Full conversation logs for review

## 🚀 Usage Examples

### JavaScript/Frontend:
```javascript
// Initial assessment
const response1 = await fetch('/api/chatbot', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    message: "I have severe headache",
    session_id: generateSessionId()
  })
});

// Follow-up with same session
const response2 = await fetch('/api/chatbot', {
  method: 'POST', 
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    message: "The headache is getting worse and I feel nauseous",
    session_id: sameSessionId // Same session for continuity
  })
});
```

### Python/Backend:
```python
import requests

session_id = "patient_session_001"

# Initial triage
response1 = requests.post('/api/health/triage', json={
    "chief_complaint": "Chest pain",
    "symptoms": ["chest pain", "shortness of breath"],
    "session_id": session_id
})

# Follow-up assessment
response2 = requests.post('/api/chatbot', json={
    "message": "The chest pain is now severe and radiating",
    "session_id": session_id  # Same session
})
```

## 📊 Monitoring & Analytics

### History Metrics:
- Average conversation length
- Escalation patterns
- Symptom progression tracking
- Response accuracy with context

### Quality Assurance:
- Context relevance scoring
- Continuity assessment
- Medical accuracy with history
- Patient satisfaction tracking

---

**🏥 The conversation history feature makes Medicura's triage agent more intelligent, contextual, and effective at providing continuous medical guidance!**