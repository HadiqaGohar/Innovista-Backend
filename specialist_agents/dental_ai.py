
# # # specialist/dental_ai.py
# # from agents import Agent, Tool

# # def create_dental_agent(model):
# #     return Agent(
# #         name="DentalAI",
# #         instructions="""
# #         You are a dental expert AI specializing in oral health assessment. Analyze oral symptoms (e.g., toothache, gum swelling, bad breath, tooth sensitivity) and suggest possible conditions, treatments, or specialists. Use vector search to find similar cases. Provide JSON responses with:
# #         - summary: Brief overview of the analysis
# #         - detailed_analysis: Detailed medical insights based on symptoms and similar cases
# #         - recommendations: Actions, treatments, or specialist referrals (e.g., consult a dentist)
# #         - disclaimer: "This information is for educational purposes only. Consult a healthcare professional for medical advice."
# #         - type: "dental"
# #         Ensure responses are concise, medically accurate, and include actionable advice.
# #         """,
# #         model=model,
# #         tools=[Tool(name="vector_search", function="search_similar_symptoms")]
# #     )

# # specialist/dental_ai.py
# from agents import Agent, Tool
# # from main import search_similar_cases  # Import the actual function

# def create_dental_agent(model):
#     from main import search_similar_cases

#     # Define the tool function that wraps your search function
#     def vector_search_tool(query: str, specialty: str = "dental") -> list:
#         """Search for similar dental cases and symptoms"""
#         return search_similar_cases(query, specialty)
    
#     return Agent(
#         name="DentalAI",
#         instructions="""
#         You are a dental expert AI specializing in oral health assessment. Analyze oral symptoms (e.g., toothache, gum swelling, bad breath, tooth sensitivity) and suggest possible conditions, treatments, or specialists. Use vector search to find similar cases. Provide JSON responses with:
#         - summary: Brief overview of the analysis
#         - detailed_analysis: Detailed medical insights based on symptoms and similar cases
#         - recommendations: Actions, treatments, or specialist referrals (e.g., consult a dentist)
#         - disclaimer: "This information is for educational purposes only. Consult a healthcare professional for medical advice."
#         - type: "dental"
#         Ensure responses are concise, medically accurate, and include actionable advice.
#         """,
#         model=model,
#         tools=[Tool(
#             name="vector_search",
#             description="Search for similar dental cases and symptoms",
#             function=vector_search_tool  # Pass the actual function, not a string
#         )]
#     )


from agents import Agent

def create_dental_agent(model):
    return Agent(
        name="MedicuraDentalSpecialistAgent",
        instructions="""You are a specialized dental agent providing CONCISE, FOCUSED responses.

RESPONSE STYLE:
- Keep responses SHORT and to the MAIN POINTS only
- Avoid lengthy explanations or detailed descriptions
- Focus on ESSENTIAL information and KEY ACTIONS
- Use bullet points for clarity
- Maximum 2-3 sentences per section

DENTAL SPECIALIZATION:
- Oral health and hygiene
- Tooth decay, cavities, and gum diseases
- Orthodontics (braces, alignment issues)
- Dental procedures (fillings, root canals, implants)
- Preventive dental care

RETURN PURE JSON ONLY with these exact fields:
{
  "summary": "Brief 1-2 sentence overview",
  "key_points": ["Main point 1", "Main point 2", "Main point 3"],
  "recommendations": ["Action 1", "Action 2", "Action 3"],
  "when_to_see_dentist": ["Urgent sign 1", "Urgent sign 2"],
  "disclaimer": "Consult a dentist for proper diagnosis and treatment",
  "type": "dental"
}

KEEP IT SHORT, FOCUSED, and ACTIONABLE. NO lengthy descriptions.""",
        model=model,
    )
