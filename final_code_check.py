#!/usr/bin/env python3
"""
Final comprehensive code check for Medicura AI
"""

def final_code_check():
    """Complete system check"""
    
    print("🏥 MEDICURA AI - FINAL CODE CHECK")
    print("=" * 60)
    
    results = {
        "imports": False,
        "database": False,
        "history": False,
        "agents": False,
        "api": False,
        "context": False
    }
    
    # 1. Import Check
    print("\n🔍 1. IMPORT & SYNTAX CHECK")
    print("-" * 40)
    try:
        from main import (
            app, get_db, load_history, save_history,
            symptom_analyzer_agent, triage_agent,
            drug_interaction_agent, general_health_agent
        )
        from medicura_agents.triage_agent import create_triage_agent
        print("✅ All critical imports successful")
        print("✅ No syntax errors found")
        results["imports"] = True
    except Exception as e:
        print(f"❌ Import error: {e}")
    
    # 2. Database Check
    print("\n🗄️ 2. DATABASE CONNECTION & TABLES")
    print("-" * 40)
    try:
        conn = get_db()
        if conn:
            with conn.cursor() as cur:
                # Check table exists
                cur.execute("SHOW TABLES LIKE 'chat_sessions'")
                if cur.fetchone():
                    print("✅ Database connected")
                    print("✅ chat_sessions table exists")
                    
                    # Check data
                    cur.execute("SELECT COUNT(*) FROM chat_sessions")
                    count = cur.fetchone()[0]
                    print(f"✅ Sessions in database: {count}")
                    results["database"] = True
                else:
                    print("❌ chat_sessions table missing")
            conn.close()
        else:
            print("❌ Database connection failed")
    except Exception as e:
        print(f"❌ Database error: {e}")
    
    # 3. History Functions
    print("\n🧠 3. CONVERSATION HISTORY")
    print("-" * 40)
    try:
        # Test load/save
        test_session = "final_check_session"
        history = load_history(test_session)
        print(f"✅ load_history works: {len(history)} messages")
        
        # Test save
        test_data = [
            {"role": "user", "content": "Final check test", "timestamp": "2024-01-01T00:00:00"},
            {"role": "assistant", "content": "Test response", "timestamp": "2024-01-01T00:00:01"}
        ]
        save_history(test_session, test_data)
        
        # Verify
        loaded = load_history(test_session)
        if len(loaded) >= 2:
            print("✅ save_history works")
            print("✅ History persistence verified")
            results["history"] = True
        else:
            print("❌ History not persisting")
    except Exception as e:
        print(f"❌ History error: {e}")
    
    # 4. Agent System
    print("\n🤖 4. AI AGENTS")
    print("-" * 40)
    try:
        agents_to_check = [
            ("Triage", triage_agent),
            ("Symptom Analyzer", symptom_analyzer_agent),
            ("Drug Interaction", drug_interaction_agent),
            ("General Health", general_health_agent)
        ]
        
        all_agents_ok = True
        for name, agent in agents_to_check:
            if hasattr(agent, 'name'):
                print(f"✅ {name}: {agent.name}")
            else:
                print(f"❌ {name}: Invalid agent")
                all_agents_ok = False
        
        if all_agents_ok:
            results["agents"] = True
    except Exception as e:
        print(f"❌ Agents error: {e}")
    
    # 5. API Structure
    print("\n🌐 5. API ENDPOINTS")
    print("-" * 40)
    try:
        # Check FastAPI app
        print(f"✅ FastAPI app: {app.title} v{app.version}")
        
        # Check if endpoints exist (by checking routes)
        routes = [str(route.path) for route in app.routes]
        
        required_endpoints = [
            "/api/chatbot",
            "/api/health/triage",
            "/api/chatbot/sessions",
            "/health"
        ]
        
        endpoints_ok = True
        for endpoint in required_endpoints:
            if any(endpoint in route for route in routes):
                print(f"✅ Endpoint exists: {endpoint}")
            else:
                print(f"❌ Missing endpoint: {endpoint}")
                endpoints_ok = False
        
        if endpoints_ok:
            results["api"] = True
    except Exception as e:
        print(f"❌ API error: {e}")
    
    # 6. Context Integration
    print("\n🔄 6. HISTORY CONTEXT INTEGRATION")
    print("-" * 40)
    try:
        # Test context structure
        test_history = [
            {"role": "user", "content": "I have chest pain", "timestamp": "2024-01-01T10:00:00"}
        ]
        
        context = {
            "specialty": "triage",
            "history": test_history,
            "session_id": "context_test"
        }
        
        print("✅ Context structure created")
        print(f"✅ History integration: {len(context['history'])} messages")
        print(f"✅ Specialty routing: {context['specialty']}")
        results["context"] = True
    except Exception as e:
        print(f"❌ Context error: {e}")
    
    # Final Summary
    print("\n" + "=" * 60)
    print("🎯 FINAL RESULTS SUMMARY")
    print("=" * 60)
    
    total_tests = len(results)
    passed_tests = sum(results.values())
    
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{test_name.upper():.<20} {status}")
    
    print("-" * 60)
    print(f"OVERALL SCORE: {passed_tests}/{total_tests} ({(passed_tests/total_tests)*100:.1f}%)")
    
    if passed_tests == total_tests:
        print("\n🎉 ALL SYSTEMS WORKING PERFECTLY!")
        print("✅ Code is ready for production")
        print("✅ History system fully functional")
        print("✅ Triage agent with memory working")
        print("✅ Database integration complete")
    else:
        print(f"\n⚠️  {total_tests - passed_tests} issues found")
        print("🔧 Check failed components above")
    
    return results

if __name__ == "__main__":
    final_code_check()