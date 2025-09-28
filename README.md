# 🏥 AI Healthcare

## 📌 Overview

**AI Healthcare** is a multi-agent AI system that connects citizens with frontline healthcare workers.  
Its main goal is to make healthcare services **efficient, fair, and accessible**.  
The system is built around **five specialized agents**, each handling a specific part of the healthcare workflow:

1. **Triage Agent (Frontline):** Analyzes case data and determines the urgency level.  
2. **Guidance Agent (Frontline):** Matches citizens with the nearest and most suitable hospital/department (Pakistan-specific).  
3. **Booking Agent (Citizen-facing):** Schedules appointments, pre-fills forms, and sets reminders.  
4. **Follow-up Agent (Citizen-facing):** Sends reminders, tracks progress, and saves appointments to Google Calendar.  
5. **Equity Oversight Agent:** Monitors demand vs. capacity and generates reports & KPIs for administrators.

---

## 📊 Data & Validation

- ✅ **220+ citizen requests** ready for testing  
- ✅ **50+ hospitals** analyzed with bed capacity and coordinates  
- ✅ All APIs tested and working correctly  


## ⚙️ Setup Instructions

- Python **3.10+**  
- Google Maps API Key  
- Google Calendar credentials  
- Streamlit (Frontend)
- Openai Agents SDK

### 🚀 Quickstart

```bash
# Clone the repository
git clone <repo-url>
cd repo

# Create a virtual environment
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
uvicorn app.main:app --reload
```

## 🧠 Summary

AI Healthcare is an AI-powered healthcare equity platform that simplifies processes for patients and doctors while giving administrators real-time, data-driven insights to improve decision-making.
