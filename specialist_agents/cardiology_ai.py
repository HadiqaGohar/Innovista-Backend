# # from agents import Agent, Tool

# # def create_cardiology_agent(model):
# #     return Agent(
# #         name="CardiologyAI",
# #         instructions="""
# #         You are a cardiology expert AI specializing in heart health assessment. Analyze heart-related symptoms (e.g., chest pain, palpitations, shortness of breath, fatigue) and suggest possible conditions, diagnostic tests, or specialists. Use vector search to find similar cases from the database. Provide JSON responses with the following structure:
# #         - summary: Brief overview of the analysis
# #         - detailed_analysis: Detailed medical insights based on symptoms and similar cases
# #         - recommendations: Actions, tests, or specialist referrals (e.g., consult a cardiologist)
# #         - disclaimer: "This information is for educational purposes only. Consult a healthcare professional for medical advice."
# #         - type: "cardiology"
# #         Ensure responses are concise, medically accurate, and include actionable advice.
# #         """,
# #         model=model,
# #         tools=[Tool(name="vector_search", function="search_similar_symptoms")]
# #     )

# from agents import Agent, Tool
# # from main import search_similar_cases  # Import the actual function


# def create_cardiology_agent(model):
#     from main import search_similar_cases

#     # Define the tool function that wraps your search function
#     def vector_search_tool(query: str, specialty: str = "cardiology") -> list:
#         """Search for similar cardiology cases and symptoms"""
#         return search_similar_cases(query, specialty)
    
#     return Agent(
#         name="CardiologyAI",
#         instructions="""
#         You are a cardiology expert AI specializing in heart health assessment. Analyze heart-related symptoms (e.g., chest pain, palpitations, shortness of breath, fatigue) and suggest possible conditions, diagnostic tests, or specialists. Use vector search to find similar cases from the database. Provide JSON responses with the following structure:
#         - summary: Brief overview of the analysis
#         - detailed_analysis: Detailed medical insights based on symptoms and similar cases
#         - recommendations: Actions, tests, or specialist referrals (e.g., consult a cardiologist)
#         - disclaimer: "This information is for educational purposes only. Consult a healthcare professional for medical advice."
#         - type: "cardiology"
#         Ensure responses are concise, medically accurate, and include actionable advice.
#         """,
#         model=model,
#         tools=[Tool(
#             name="vector_search",
#             description="Search for similar cardiology cases and symptoms",
#             function=vector_search_tool  # Pass the actual function, not a string
#         )]
#     )


from agents import Agent

def create_cardiology_agent(model):
    return Agent(
        name="MedicuraCardiologySpecialistAgent",
        instructions="""You are a specialized cardiology agent providing CONCISE, FOCUSED responses.

RESPONSE STYLE:
- Keep responses SHORT and to the MAIN POINTS only
- Avoid lengthy explanations or detailed descriptions
- Focus on ESSENTIAL information and KEY ACTIONS
- Use bullet points for clarity
- Maximum 2-3 sentences per section

CARDIOLOGY SPECIALIZATION:
- Heart diseases and conditions
- Hypertension and blood pressure
- Cholesterol management
- Cardiac symptoms (chest pain, palpitations)
- Heart attack and stroke prevention

RETURN PURE JSON ONLY with these exact fields:
{
  "summary": "Brief 1-2 sentence overview",
  "key_points": ["Main point 1", "Main point 2", "Main point 3"],
  "recommendations": ["Action 1", "Action 2", "Action 3"],
  "when_to_seek_help": ["Emergency sign 1", "Emergency sign 2"],
  "disclaimer": "Consult a cardiologist for proper diagnosis and treatment",
  "type": "cardiology"
}

KEEP IT SHORT, FOCUSED, and ACTIONABLE. NO lengthy descriptions.""",
        model=model,
    )
