# 🔍 Conversation History Check Guide

Yeh guide aapko step-by-step batayega ke conversation history kaise check karni hai.

## 🚀 Quick Check (Sabse Pehle Yeh Try Karein)

### 1. Server Start Karein:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Quick Check Run Karein:
```bash
python quick_history_check.py
```

Yeh aapko turant bata dega ke history working hai ya nahi.

## 📋 Detailed Testing (Step by Step)

### Method 1: Automated Testing
```bash
# Complete step-by-step test
python test_history_step_by_step.py

# Database direct check
python check_history.py
```

### Method 2: Manual API Testing

#### Step 1: Send First Message
```bash
curl -X POST "http://localhost:8000/api/chatbot" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "I have chest pain",
    "session_id": "test_session_123"
  }'
```

#### Step 2: Send Follow-up Message (Same Session)
```bash
curl -X POST "http://localhost:8000/api/chatbot" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "The pain is getting worse",
    "session_id": "test_session_123"
  }'
```

#### Step 3: Check History
```bash
curl "http://localhost:8000/api/chatbot/session/test_session_123/history"
```

#### Step 4: View All Sessions
```bash
curl "http://localhost:8000/api/chatbot/sessions"
```

## 🔧 Database Direct Check

### Using Python Script:
```bash
python check_history.py
```

### Manual Database Check:
```python
import pymysql
import json
import os
from dotenv import load_dotenv

load_dotenv()

# Connect to database
conn = pymysql.connect(
    host=os.getenv("TIDB_HOST"),
    port=4000,
    user=os.getenv("TIDB_USERNAME"),
    password=os.getenv("TIDB_PASSWORD"),
    database=os.getenv("TIDB_DATABASE"),
    charset="utf8mb4",
    ssl={"ssl_mode": "VERIFY_IDENTITY"}
)

# Check sessions
with conn.cursor() as cur:
    cur.execute("SELECT session_id, last_updated FROM chat_sessions")
    sessions = cur.fetchall()
    print(f"Total sessions: {len(sessions)}")
    
    for session_id, last_updated in sessions:
        print(f"Session: {session_id}, Updated: {last_updated}")

conn.close()
```

## 🌐 Browser Testing

### 1. Open API Documentation:
```
http://localhost:8000/api/docs
```

### 2. Test Endpoints:
- **POST** `/api/chatbot` - Send messages
- **GET** `/api/chatbot/sessions` - View all sessions  
- **GET** `/api/chatbot/session/{session_id}/history` - View specific history

### 3. Direct Browser URLs:
```
http://localhost:8000/api/chatbot/sessions
http://localhost:8000/api/chatbot/session/test_session_123/history
```

## ✅ What to Look For

### History Working Signs:
- ✅ **Sessions List**: `/api/chatbot/sessions` shows sessions
- ✅ **Message Count**: Each session shows message count > 0
- ✅ **History Content**: `/api/chatbot/session/{id}/history` shows messages
- ✅ **Timestamps**: Each message has timestamp
- ✅ **Role Separation**: Messages marked as "user" or "assistant"

### Example Working Response:
```json
{
  "session_id": "test_session_123",
  "total_messages": 4,
  "history": [
    {
      "role": "user",
      "content": "I have chest pain",
      "timestamp": "2024-01-15T10:30:00"
    },
    {
      "role": "assistant",
      "content": "{\"triage_level\": \"HIGH\", \"summary\": \"Chest pain assessment\"}",
      "timestamp": "2024-01-15T10:30:15",
      "summary": "Chest pain assessment",
      "triage_level": "HIGH"
    }
  ]
}
```

## 🚨 Troubleshooting

### Problem: No Sessions Found
```bash
# Check if table exists
python check_history.py
# Select option 1 to check table structure
```

### Problem: Messages Not Saving
```bash
# Check database connection
python -c "
from main import get_db
conn = get_db()
print('Database connected!' if conn else 'Connection failed!')
"
```

### Problem: History Not Loading
```bash
# Test load_history function
python -c "
from main import load_history
history = load_history('test_session')
print(f'History loaded: {len(history)} messages')
"
```

## 📊 Expected Results

### After Sending 2 Messages:
- **Total Sessions**: 1
- **Message Count**: 4 (2 user + 2 assistant)
- **History API**: Returns formatted conversation
- **Database**: Contains JSON history data

### Conversation Flow:
1. **User**: "I have chest pain" → **Agent**: HIGH priority assessment
2. **User**: "Getting worse" → **Agent**: CRITICAL priority (references previous)

## 🔗 Useful Commands

### Quick Status Check:
```bash
# Check server
curl http://localhost:8000/health

# Check sessions count
curl http://localhost:8000/api/chatbot/sessions | jq '.total_sessions'

# Check specific session
curl http://localhost:8000/api/chatbot/session/YOUR_SESSION_ID/history | jq '.total_messages'
```

### Database Query:
```sql
-- Direct SQL check (if you have database access)
SELECT session_id, JSON_LENGTH(history) as message_count, last_updated 
FROM chat_sessions 
ORDER BY last_updated DESC;
```

## 💡 Pro Tips

1. **Use Consistent Session IDs**: Same session_id = same conversation
2. **Check Timestamps**: Verify messages are being saved with correct time
3. **Test Different Sessions**: Ensure isolation between users
4. **Monitor Database**: Watch for new entries after each message
5. **Use Browser DevTools**: Check network requests for session_id

## 🎯 Success Criteria

History is working correctly if:
- ✅ Messages appear in `/api/chatbot/sessions`
- ✅ Individual history shows in `/api/chatbot/session/{id}/history`
- ✅ Follow-up messages reference previous context
- ✅ Different sessions remain isolated
- ✅ Database contains JSON conversation data

---

**🏥 Use these tools to verify your Medicura conversation history is working perfectly!**