#!/usr/bin/env python3
"""
Test script for the Triage Agent
"""

import asyncio
import json
from medicura_agents.triage_agent import create_triage_agent
from agents import OpenAIChatCompletionsModel, ModelSettings, RunConfig, Runner, AsyncOpenAI
import httpx
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def test_triage_agent():
    """Test the triage agent with sample cases"""
    
    # Initialize the model and agent
    external_client = AsyncOpenAI(
        api_key=os.getenv("GEMINI_API_KEY"),
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
        http_client=httpx.AsyncClient(timeout=60.0)
    )

    model = OpenAIChatCompletionsModel(
        model="gemini-2.0-flash",
        openai_client=external_client,
    )

    model_settings = ModelSettings(
        temperature=0.7,
        top_p=0.9,
        max_tokens=2048,
    )

    config = RunConfig(
        model=model,
        model_provider=external_client,
        model_settings=model_settings,
        tracing_disabled=True,
    )

    # Create triage agent
    triage_agent = create_triage_agent(model)
    
    # Test cases
    test_cases = [
        {
            "name": "Critical Emergency - Chest Pain",
            "prompt": """
            TRIAGE ASSESSMENT REQUEST:
            
            Chief Complaint: Severe chest pain
            Symptoms: crushing chest pain, shortness of breath, sweating, nausea
            Duration: Started 30 minutes ago
            Severity: Severe (9/10)
            Age: 55 years
            Gender: Male
            Pain Level: 9/10
            Additional Information: Pain radiating to left arm, patient appears pale and diaphoretic
            """
        },
        {
            "name": "High Priority - Severe Headache",
            "prompt": """
            TRIAGE ASSESSMENT REQUEST:
            
            Chief Complaint: Worst headache of my life
            Symptoms: sudden severe headache, neck stiffness, sensitivity to light
            Duration: Started 2 hours ago suddenly
            Severity: Severe (10/10)
            Age: 35 years
            Gender: Female
            Pain Level: 10/10
            """
        },
        {
            "name": "Medium Priority - Fever and Cough",
            "prompt": """
            TRIAGE ASSESSMENT REQUEST:
            
            Chief Complaint: Fever and persistent cough
            Symptoms: fever, dry cough, fatigue, mild shortness of breath
            Duration: 3 days
            Severity: Moderate
            Age: 28 years
            Gender: Female
            Pain Level: 3/10
            """
        },
        {
            "name": "Low Priority - Minor Cut",
            "prompt": """
            TRIAGE ASSESSMENT REQUEST:
            
            Chief Complaint: Small cut on finger
            Symptoms: minor bleeding, small laceration
            Duration: Just happened
            Severity: Mild
            Age: 25 years
            Gender: Male
            Pain Level: 2/10
            Additional Information: Cut while cooking, bleeding has mostly stopped
            """
        }
    ]
    
    print("🏥 Testing Medicura Triage Agent")
    print("=" * 50)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📋 Test Case {i}: {test_case['name']}")
        print("-" * 40)
        
        try:
            # Run the triage agent
            result = await Runner.run(triage_agent, test_case['prompt'], run_config=config)
            
            # Try to parse as JSON
            try:
                response_json = json.loads(result.final_output)
                print(f"✅ Triage Level: {response_json.get('triage_level', 'N/A')}")
                print(f"🔢 Urgency Score: {response_json.get('urgency_score', 'N/A')}/10")
                print(f"📍 Routing: {response_json.get('routing_decision', 'N/A')}")
                print(f"⏰ Time Frame: {response_json.get('time_frame', 'N/A')}")
                print(f"📝 Summary: {response_json.get('case_summary', 'N/A')}")
                
                if response_json.get('red_flags'):
                    print(f"🚨 Red Flags: {', '.join(response_json['red_flags'])}")
                    
            except json.JSONDecodeError:
                print("⚠️  Response not in JSON format:")
                print(result.final_output[:300] + "..." if len(result.final_output) > 300 else result.final_output)
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")
    
    print("\n" + "=" * 50)
    print("🎯 Triage Agent Testing Complete!")

if __name__ == "__main__":
    asyncio.run(test_triage_agent())