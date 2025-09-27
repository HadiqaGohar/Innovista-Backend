#!/usr/bin/env python3
"""
Update all specialist agents to provide concise responses
"""

import os
import glob

def update_specialist_agent(file_path, specialty_name, specialty_focus):
    """Update a specialist agent file with concise instructions"""
    
    agent_name = f"Medicura{specialty_name}SpecialistAgent"
    
    new_content = f'''from agents import Agent

def create_{specialty_name.lower()}_agent(model):
    return Agent(
        name="{agent_name}",
        instructions="""You are a specialized {specialty_name.lower()} agent providing CONCISE, FOCUSED responses.

RESPONSE STYLE:
- Keep responses SHORT and to the MAIN POINTS only
- Avoid lengthy explanations or detailed descriptions
- Focus on ESSENTIAL information and KEY ACTIONS
- Use bullet points for clarity
- Maximum 2-3 sentences per section

{specialty_name.upper()} SPECIALIZATION:
{specialty_focus}

RETURN PURE JSON ONLY with these exact fields:
{{
  "summary": "Brief 1-2 sentence overview",
  "key_points": ["Main point 1", "Main point 2", "Main point 3"],
  "recommendations": ["Action 1", "Action 2", "Action 3"],
  "when_to_seek_help": ["Warning sign 1", "Warning sign 2"],
  "disclaimer": "Consult a {specialty_name.lower()} specialist for proper diagnosis and treatment",
  "type": "{specialty_name.lower()}"
}}

KEEP IT SHORT, FOCUSED, and ACTIONABLE. NO lengthy descriptions.""",
        model=model,
    )
'''
    
    with open(file_path, 'w') as f:
        f.write(new_content)
    
    print(f"✅ Updated {specialty_name} agent")

def main():
    """Update all specialist agents"""
    
    print("🔄 UPDATING ALL SPECIALIST AGENTS")
    print("=" * 50)
    
    # Define specialties and their focus areas
    specialties = {
        "neurology": """- Brain and nervous system disorders
- Headaches, migraines, seizures
- Stroke and neurological symptoms
- Memory and cognitive issues
- Nerve pain and numbness""",
        
        "pulmonology": """- Lung and respiratory conditions
- Asthma, COPD, bronchitis
- Breathing difficulties and cough
- Chest infections and pneumonia
- Sleep apnea and breathing disorders""",
        
        "ophthalmology": """- Eye health and vision problems
- Eye infections and injuries
- Vision changes and eye pain
- Glaucoma, cataracts, retinal issues
- Eye care and prevention""",
        
        "allergy_immunology": """- Allergic reactions and sensitivities
- Food, drug, and environmental allergies
- Asthma and allergic conditions
- Immune system disorders
- Allergy testing and management""",
        
        "pediatrics": """- Child health and development
- Childhood illnesses and infections
- Growth and developmental concerns
- Pediatric emergencies
- Child vaccination and preventive care""",
        
        "orthopedics": """- Bone, joint, and muscle problems
- Fractures, sprains, and injuries
- Arthritis and joint pain
- Back and neck problems
- Sports injuries and rehabilitation""",
        
        "mental_health": """- Mental health and emotional wellbeing
- Depression, anxiety, and mood disorders
- Stress management and coping
- Sleep disorders and mental health
- Crisis intervention and support""",
        
        "endocrinology": """- Hormone-related disorders
- Diabetes and blood sugar management
- Thyroid and metabolic conditions
- Weight management and obesity
- Hormonal imbalances""",
        
        "gastroenterology": """- Digestive system disorders
- Stomach pain, nausea, and indigestion
- Bowel problems and constipation
- Liver and gallbladder issues
- Dietary and digestive health""",
        
        "radiology": """- Medical imaging interpretation
- X-ray, CT, MRI, and ultrasound results
- Imaging recommendations
- Diagnostic imaging guidance
- Radiology report explanations""",
        
        "infectious_disease": """- Infections and contagious diseases
- Bacterial, viral, and fungal infections
- Fever and infection symptoms
- Antibiotic and antiviral treatments
- Infection prevention and control""",
        
        "vaccination_advisor": """- Vaccination schedules and recommendations
- Vaccine safety and side effects
- Travel vaccinations
- Adult and pediatric immunizations
- Vaccine contraindications and precautions"""
    }
    
    # Update each specialist agent
    for specialty, focus in specialties.items():
        file_path = f"specialist_agents/{specialty}_ai.py"
        if os.path.exists(file_path):
            update_specialist_agent(file_path, specialty.replace('_', ' ').title().replace(' ', ''), focus)
        else:
            print(f"⚠️  File not found: {file_path}")
    
    print("\n" + "=" * 50)
    print("🎯 ALL SPECIALIST AGENTS UPDATED!")
    print("✅ Now providing concise, focused responses")
    print("✅ Short main points instead of detailed descriptions")
    print("✅ Actionable recommendations")

if __name__ == "__main__":
    main()