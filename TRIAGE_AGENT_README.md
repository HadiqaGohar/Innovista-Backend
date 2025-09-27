# 🏥 Medicura Triage Agent

The Triage Agent is a frontline medical assessment AI that analyzes case data and determines urgency levels for appropriate care routing.

## 🎯 Purpose

- **Rapid Assessment**: Quickly evaluate medical cases and symptoms
- **Urgency Determination**: Assign appropriate triage levels (CRITICAL, HIGH, MEDIUM, LOW)
- **Care Routing**: Direct patients to the right level of care
- **Emergency Detection**: Identify life-threatening conditions requiring immediate attention

## 🚨 Triage Levels

### CRITICAL (Urgency 9-10)
- **Examples**: Cardiac arrest, stroke, severe trauma, anaphylaxis
- **Action**: Call emergency services immediately
- **Time Frame**: Immediate intervention required

### HIGH (Urgency 7-8)
- **Examples**: Chest pain, severe abdominal pain, high fever with systemic symptoms
- **Action**: Emergency Department within 1-2 hours
- **Time Frame**: Same day urgent care

### MEDIUM (Urgency 4-6)
- **Examples**: Moderate pain, stable infections, minor injuries
- **Action**: Urgent care or primary care within 24 hours
- **Time Frame**: Next day appointment

### LOW (Urgency 1-3)
- **Examples**: Minor aches, routine care, medication refills
- **Action**: Primary care or telehealth
- **Time Frame**: Within 1-7 days

## 📋 API Endpoints

### 1. Dedicated Triage Endpoint
```http
POST /api/health/triage
```

**Request Body:**
```json
{
  "chief_complaint": "Severe chest pain",
  "symptoms": ["chest pain", "shortness of breath", "sweating"],
  "duration": "30 minutes",
  "severity": "severe",
  "age": 55,
  "gender": "male",
  "pain_level": 9,
  "vital_signs": {
    "blood_pressure": "160/95",
    "heart_rate": 110
  },
  "medical_history": ["hypertension", "diabetes"],
  "current_medications": ["metformin", "lisinopril"],
  "additional_info": "Pain radiating to left arm"
}
```

**Response:**
```json
{
  "triage_level": "CRITICAL",
  "urgency_score": 9,
  "case_summary": "55-year-old male with acute chest pain and cardiac risk factors",
  "primary_concern": "Possible acute coronary syndrome",
  "recommended_action": "Call emergency services immediately",
  "time_frame": "Immediate",
  "red_flags": ["chest pain with radiation", "diaphoresis", "cardiac risk factors"],
  "routing_decision": "Emergency Department",
  "reasoning": "Classic presentation of acute coronary syndrome with multiple risk factors",
  "disclaimer": "This triage assessment is for guidance only...",
  "type": "triage"
}
```

### 2. Chat Integration
The triage agent is automatically triggered in the main chatbot when users mention:
- "emergency", "urgent", "triage"
- "how urgent", "priority", "serious"
- "critical", "immediate care"
- "emergency room", "er", "911", "1122"

## 🔍 Key Features

### Red Flag Detection
Automatically identifies concerning symptoms:
- Chest pain with cardiac features
- Stroke symptoms (FAST protocol)
- Severe allergic reactions
- High fever with systemic symptoms
- Severe trauma or bleeding
- Mental health emergencies

### Special Population Considerations
- **Pediatric**: Lower threshold for higher triage
- **Geriatric**: Consider frailty and comorbidities
- **Pregnancy**: Obstetric complications prioritized
- **Immunocompromised**: Higher infection risk

### Safety Protocols
- **Conservative Approach**: When in doubt, triage higher
- **Clear Instructions**: Specific actionable guidance
- **Emergency Routing**: Direct path to appropriate care
- **Documentation**: Reasoning provided for audit

## 🧪 Testing

Run the test script to verify functionality:

```bash
python test_triage_agent.py
```

This will test various scenarios:
- Critical emergency (chest pain)
- High priority (severe headache)
- Medium priority (fever/cough)
- Low priority (minor cut)

## ⚠️ Important Notes

1. **Not a Replacement**: This is a triage tool, not a diagnostic system
2. **Professional Consultation**: Always recommend professional medical evaluation
3. **Emergency Override**: Any life-threatening symptoms should bypass triage
4. **Documentation**: All assessments should be logged for quality assurance

## 🔧 Integration

The triage agent is integrated into:
- Main chatbot (`/api/chatbot`)
- Dedicated endpoint (`/api/health/triage`)
- Automatic keyword detection
- Session history tracking

## 📞 Emergency Contacts

The agent provides appropriate emergency contact information:
- **Pakistan**: 1122 (Emergency Services)
- **International**: Local emergency numbers
- **Poison Control**: Relevant hotlines

## 🛡️ Disclaimer

This triage assessment tool is for guidance only and does not replace professional medical evaluation. If you believe this is a medical emergency, call emergency services immediately.