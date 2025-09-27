#!/usr/bin/env python3
"""
Startup test to verify all components are working
"""

def test_imports():
    """Test all critical imports"""
    print("🔍 Testing imports...")
    
    try:
        # Test basic imports
        import os
        import json
        from datetime import datetime
        from fastapi import FastAPI
        print("✅ Basic imports successful")
        
        # Test agent imports
        from agents import Agent, Runner, RunConfig, AsyncOpenAI, OpenAIChatCompletionsModel, ModelSettings
        print("✅ Agent framework imports successful")
        
        # Test medicura agents
        from medicura_agents.symptom_analyzer_agent import create_symptom_analyzer_agent
        from medicura_agents.triage_agent import create_triage_agent
        print("✅ Medicura agents imports successful")
        
        # Test main app
        from main import app
        print("✅ Main app import successful")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_agent_creation():
    """Test agent creation"""
    print("\n🤖 Testing agent creation...")
    
    try:
        import os
        import httpx
        from agents import AsyncOpenAI, OpenAIChatCompletionsModel, ModelSettings
        from medicura_agents.triage_agent import create_triage_agent
        from dotenv import load_dotenv
        
        load_dotenv()
        
        # Create mock model (without API call)
        external_client = AsyncOpenAI(
            api_key=os.getenv("GEMINI_API_KEY", "test-key"),
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
            http_client=httpx.AsyncClient(timeout=60.0)
        )

        model = OpenAIChatCompletionsModel(
            model="gemini-2.0-flash",
            openai_client=external_client,
        )
        
        # Test agent creation
        triage_agent = create_triage_agent(model)
        print("✅ Triage agent created successfully")
        print(f"✅ Agent name: {triage_agent.name}")
        
        return True
        
    except Exception as e:
        print(f"❌ Agent creation error: {e}")
        return False

def test_pydantic_models():
    """Test Pydantic models"""
    print("\n📋 Testing Pydantic models...")
    
    try:
        from main import TriageRequest
        
        # Test model creation
        test_request = TriageRequest(
            chief_complaint="Test complaint",
            symptoms=["symptom1", "symptom2"],
            age=30,
            gender="male"
        )
        
        print("✅ TriageRequest model working")
        print(f"✅ Chief complaint: {test_request.chief_complaint}")
        
        return True
        
    except Exception as e:
        print(f"❌ Pydantic model error: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Medicura Triage Agent Startup Test")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_agent_creation,
        test_pydantic_models
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} passed")
    
    if passed == total:
        print("🎉 All tests passed! Triage agent is ready to use.")
        print("\n🚀 To start the server:")
        print("   uvicorn main:app --reload --host 0.0.0.0 --port 8000")
        print("\n📡 Test the API:")
        print("   python test_api.py")
    else:
        print("❌ Some tests failed. Please check the errors above.")

if __name__ == "__main__":
    main()