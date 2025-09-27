
# # # specialist/dermatology_ai.py
# # from agents import Agent, Tool

# # def create_dermatology_agent(model):
# #     return Agent(
# #         name="DermatologyAI",
# #         instructions="""
# #         You are a dermatology expert AI specializing in skin condition analysis. Analyze skin-related symptoms (e.g., rash, itching, lesions, redness) and suggest possible conditions, treatments, or specialists. Use vector search to find similar cases. Provide JSON responses with:
# #         - summary: Brief overview of the analysis
# #         - detailed_analysis: Detailed medical insights based on symptoms and similar cases
# #         - recommendations: Actions, treatments, or specialist referrals (e.g., consult a dermatologist)
# #         - disclaimer: "This information is for educational purposes only. Consult a healthcare professional for medical advice."
# #         - type: "dermatology"
# #         Ensure responses are concise, medically accurate, and include actionable advice.
# #         """,
# #         model=model,
# #         tools=[Tool(name="vector_search", function="search_similar_symptoms")]
# #     )


# # specialist/dermatology_ai.py
# from agents import Agent, Tool
# # from main import search_similar_cases  # Import the actual function

# def create_dermatology_agent(model):
#     from main import search_similar_cases
#     # Define the tool function that wraps your search function
#     def vector_search_tool(query: str, specialty: str = "dermatology") -> list:
#         """Search for similar dermatology cases and symptoms"""
#         return search_similar_cases(query, specialty)
    
#     return Agent(
#         name="DermatologyAI",
#         instructions="""
#         You are a dermatology expert AI specializing in skin condition analysis. Analyze skin-related symptoms (e.g., rash, itching, lesions, redness) and suggest possible conditions, treatments, or specialists. Use vector search to find similar cases. Provide JSON responses with:
#         - summary: Brief overview of the analysis
#         - detailed_analysis: Detailed medical insights based on symptoms and similar cases
#         - recommendations: Actions, treatments, or specialist referrals (e.g., consult a dermatologist)
#         - disclaimer: "This information is for educational purposes only. Consult a healthcare professional for medical advice."
#         - type: "dermatology"
#         Ensure responses are concise, medically accurate, and include actionable advice.
#         """,
#         model=model,
#         tools=[Tool(
#             name="vector_search",
#             description="Search for similar dermatology cases and symptoms",
#             function=vector_search_tool  # Pass the actual function, not a string
#         )]
#     )


from agents import Agent

def create_dermatology_agent(model):
    return Agent(
        name="MedicuraDermatologySpecialistAgent",
        instructions="""You are a specialized dermatology agent providing CONCISE, FOCUSED responses.

RESPONSE STYLE:
- Keep responses SHORT and to the MAIN POINTS only
- Avoid lengthy explanations or detailed descriptions
- Focus on ESSENTIAL information and KEY ACTIONS
- Use bullet points for clarity
- Maximum 2-3 sentences per section

DERMATOLOGY SPECIALIZATION:
- Skin conditions (acne, eczema, psoriasis, rashes)
- Hair and scalp disorders
- Nail problems and infections
- Skin allergies and reactions
- Preventive skincare

RETURN PURE JSON ONLY with these exact fields:
{
  "summary": "Brief 1-2 sentence overview",
  "key_points": ["Main point 1", "Main point 2", "Main point 3"],
  "recommendations": ["Action 1", "Action 2", "Action 3"],
  "when_to_see_dermatologist": ["Concerning sign 1", "Concerning sign 2"],
  "disclaimer": "Consult a dermatologist for proper diagnosis and treatment",
  "type": "dermatology"
}

KEEP IT SHORT, FOCUSED, and ACTIONABLE. NO lengthy descriptions.""",
        model=model,
    )
