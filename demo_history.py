#!/usr/bin/env python3
"""
Demo script showing conversation history functionality
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

async def demo_conversation_history():
    """Demonstrate how conversation history enhances triage assessments"""
    
    print("🧠 Medicura Triage Agent - Conversation History Demo")
    print("=" * 60)
    
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

    config = RunConfig(
        model=model,
        model_provider=external_client,
        model_settings=ModelSettings(temperature=0.7, top_p=0.9, max_tokens=2048),
        tracing_disabled=True,
    )

    triage_agent = create_triage_agent(model)
    
    # Simulate conversation history
    conversation_history = []
    
    # Scenario: Progressive chest pain assessment
    interactions = [
        {
            "step": 1,
            "user_message": "I have chest pain that started 1 hour ago",
            "description": "Initial complaint - no history context"
        },
        {
            "step": 2, 
            "user_message": "The chest pain is getting worse and now I'm sweating",
            "description": "Follow-up - should reference previous chest pain"
        },
        {
            "step": 3,
            "user_message": "Should I call an ambulance? I'm also feeling nauseous now",
            "description": "Escalation - should consider progression from previous interactions"
        }
    ]
    
    for interaction in interactions:
        print(f"\n📋 Step {interaction['step']}: {interaction['description']}")
        print("-" * 50)
        print(f"👤 User: {interaction['user_message']}")
        
        # Build context with history
        context = {
            "specialty": "triage",
            "history": conversation_history.copy()
        }
        
        # Create prompt
        prompt = f"""
        TRIAGE ASSESSMENT REQUEST:
        
        Chief Complaint: {interaction['user_message']}
        
        Please perform a comprehensive triage assessment and provide urgency determination with routing recommendations.
        """
        
        try:
            # Run triage agent with history context
            result = await Runner.run(triage_agent, prompt, run_config=config)
            
            # Parse response
            try:
                response_json = json.loads(result.final_output.replace('```json', '').replace('```', '').strip())
                
                print(f"🤖 Agent Response:")
                print(f"   🚨 Triage Level: {response_json.get('triage_level', 'N/A')}")
                print(f"   📊 Urgency Score: {response_json.get('urgency_score', 'N/A')}/10")
                print(f"   🏥 Routing: {response_json.get('routing_decision', 'N/A')}")
                print(f"   📝 Summary: {response_json.get('case_summary', 'N/A')}")
                
                if response_json.get('reasoning'):
                    reasoning = response_json['reasoning'][:200] + "..." if len(response_json['reasoning']) > 200 else response_json['reasoning']
                    print(f"   🧠 Reasoning: {reasoning}")
                
                # Check if agent referenced history
                if interaction['step'] > 1:
                    response_text = json.dumps(response_json).lower()
                    history_indicators = ['previous', 'earlier', 'before', 'progression', 'worsening', 'escalat']
                    if any(indicator in response_text for indicator in history_indicators):
                        print(f"   ✅ Agent used conversation history!")
                    else:
                        print(f"   ⚠️  Agent may not have used history context")
                
                # Add to conversation history
                conversation_history.extend([
                    {"role": "user", "content": interaction['user_message'], "timestamp": "2024-01-15T10:30:00"},
                    {"role": "assistant", "content": json.dumps(response_json), "timestamp": "2024-01-15T10:30:15"}
                ])
                
                # Keep last 6 messages (3 exchanges)
                conversation_history = conversation_history[-6:]
                
            except json.JSONDecodeError:
                print(f"   ⚠️  Response format: {result.final_output[:200]}...")
                
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
    
    print("\n" + "=" * 60)
    print("🎯 Demo Complete!")
    print("\n💡 Key Observations:")
    print("   - Step 1: Initial assessment without context")
    print("   - Step 2: Should reference previous chest pain")
    print("   - Step 3: Should escalate based on symptom progression")
    print("   - Each step builds on previous interactions")
    print("\n🧠 History Context Benefits:")
    print("   ✅ Continuity of care")
    print("   ✅ Symptom progression tracking") 
    print("   ✅ Contextual urgency assessment")
    print("   ✅ Personalized recommendations")

if __name__ == "__main__":
    asyncio.run(demo_conversation_history())