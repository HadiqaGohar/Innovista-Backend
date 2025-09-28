from agents import (  # type: ignore
    Agent,
    Runner,
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
    function_tool,
    enable_verbose_stdout_logging,
    SQLiteSession
)
from agents.run import RunConfig  # type: ignore
from dotenv import load_dotenv
from pydantic import BaseModel  # type: ignore
import pandas as pd
import os
import asyncio
import json
import pdfplumber   # for extracting text from PDF

# ------------ ENV SETUP ------------
load_dotenv()

key = os.getenv("GEMINI_API_KEY")
if not key:
    raise ValueError("API key is not set in the environment variables.")

session = SQLiteSession("conversations_123", "conversations_practice.db")

# ------------ Example Input Model (not used directly yet) ------------
class UserInput(BaseModel):
    user_input: str
    urgent: bool
    need: str

# ------------ OpenAI / Gemini Client Setup ------------
Externl_client: AsyncOpenAI = AsyncOpenAI(
    api_key=key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)
model: OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=Externl_client,
)

config: RunConfig = RunConfig(
    model=model,
    model_provider=Externl_client,
    tracing_disabled=False,
)

# ------------ Tool 1: Hospitals by City (from CSV) ------------
@function_tool
def get_hospital_by_city(city: str) -> str:
    """
    Find hospitals from the CSV dataset by city name.
    Always returns JSON string.
    """
    try:
        df = pd.read_csv("pakistan (1).csv")
        results = df[df["City"].str.contains(city, case=False, na=False)]
        if results.empty:
            return f'{{"message": "No hospitals found in {city}"}}'
        return results.to_json(orient="records")
    except Exception as e:
        return f'{{"error": "{str(e)}"}}'

# ------------ Tool 2: Match Request to Service (from JSON mapping) ------------
@function_tool
def match_request_to_service(request: str) -> str:
    """
    Match citizen request to appropriate service/department using JSON dataset.
    """
    try:
        with open("frontline_worker_requests_clean_220.json", "r", encoding="utf-8") as f:
            data = json.load(f)

        # Simple keyword search in request_text
        matches = []
        for item in data:
            if request.lower() in item["request_text"].lower():
                matches.append({
                    "case_id": item["case_id"],
                    "request_type": item["request_type"],
                    "location": item["citizen_profile"]["location"]
                })
        if matches:
            return json.dumps(matches, indent=2)
        else:
            return "No direct match found in requests dataset."
    except Exception as e:
        return f'{{"error": "{str(e)}"}}'

# ------------ Tool 3: Isolation Wards (from PDF) ------------
@function_tool
def get_isolation_wards(province: str) -> str:
    """
    Returns list of COVID-19 Isolation Wards in given province from PDF dataset.
    """
    try:
        wards = []
        with pdfplumber.open("List-of-Province-wise-COVID-19-Hospital-Isolation-Wards-Pakistan.pdf") as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if province.lower() in text.lower():
                    lines = text.split("\n")
                    for line in lines:
                        if any(word in line for word in ["Hospital", "Institute", "Medical", "Civil", "DHQ", "THQ"]):
                            wards.append(line.strip())
        if wards:
            return json.dumps(wards, indent=2)
        else:
            return f"No isolation ward data found for {province}"
    except Exception as e:
        return f'{{"error": "{str(e)}"}}'

# ------------ AGENT SETUP ------------
Guidance_Agent: Agent = Agent(
    name="Guidance_Agent",
    instructions=(
        "You are a Guidance Agent. User ke input se hamesha city ka naam nikalna hai. "
        "Phir get_hospital_by_city tool ko call karna hai aur results user ko dikhana hai. "
        "Aap kabhi bhi 'mujhe maloom nahi hai' ya 'city batayein' na bolen. "
        "Agar city clear nahi ho to user se city puchho, warna tool zaroor call karo. "
        "Agar user illness/requirement bataye to match_request_to_service bhi use karo. "
        "Agar specifically isolation ward ka poochhe aur city na mile, to get_isolation_wards se province ka data do."
    ),
    model=model,
    tools=[get_hospital_by_city, match_request_to_service, get_isolation_wards],
)

# ------------ MAIN RUNNER ------------
async def main():
    user_query = "punjab ke isolation wards dhoondo."
    result = await Runner.run(
        Guidance_Agent,
        user_query,
        run_config=config,
    )
    print("\n🟢 Final Agent Output:")
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())





# from agents import (  # type: ignore
#     Agent,
#     Runner,
#     AsyncOpenAI,
#     OpenAIChatCompletionsModel,
#     function_tool,
#     enable_verbose_stdout_logging,
#     SQLiteSession,
# )
# from agents.run import RunConfig  # type: ignore
# from dotenv import load_dotenv
# from pydantic import BaseModel  # type: ignore
# import pandas as pd
# import os
# import asyncio
# import json
# import pdfplumber  # for extracting text from PDF

# # ------------ ENV SETUP ------------
# load_dotenv()

# key = os.getenv("GEMINI_API_KEY")
# if not key:
#     raise ValueError("API key is not set in the environment variables.")

# session = SQLiteSession("conversations_123", "conversations_practice.db")


# # ------------ Example Input Model (not used directly yet) ------------
# class UserInput(BaseModel):
#     user_input: str
#     urgent: bool
#     need: str


# # ------------ OpenAI / Gemini Client Setup ------------
# Externl_client: AsyncOpenAI = AsyncOpenAI(
#     api_key=key,
#     base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
# )
# model: OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(
#     model="gemini-2.5-flash",
#     openai_client=Externl_client,
# )

# config: RunConfig = RunConfig(
#     model=model,
#     model_provider=Externl_client,
#     tracing_disabled=False,
# )


# # ------------ Tool 1: Hospitals by City (from CSV) ------------
# @function_tool
# def get_hospital_by_city(city: str) -> str:
#     """
#     Find hospitals from the CSV dataset by city name.
#     Always returns JSON string.
#     """
#     try:
#         df = pd.read_csv("pakistan (1).csv")
#         results = df[df["City"].str.contains(city, case=False, na=False)]
#         if results.empty:
#             return json.dumps(
#                 {"message": f"{city} mein koi hospital ka data nahi mila."}
#             )
#         return results.to_json(orient="records")
#     except FileNotFoundError:
#         return json.dumps(
#             {
#                 "message": "Hospital ka data abhi available nahi hai. Aap province ka naam dein to mai isolation wards bata sakta hoon."
#             }
#         )
#     except Exception:
#         return json.dumps({"message": "Kuch masla aaya hai, dobara koshish karein."})


# # ------------ Tool 2: Match Request to Service (from JSON mapping) ------------
# @function_tool
# def match_request_to_service(request: str) -> str:
#     try:
#         with open(
#             "frontline_worker_requests_clean_220.json", "r", encoding="utf-8"
#         ) as f:
#             data = json.load(f)

#         matches = []
#         for item in data:
#             if request.lower() in item["request_text"].lower():
#                 matches.append(
#                     {
#                         "case_id": item["case_id"],
#                         "request_type": item["request_type"],
#                         "location": item["citizen_profile"]["location"],
#                     }
#                 )
#         if matches:
#             return json.dumps(matches, indent=2)
#         else:
#             return json.dumps({"message": "Is request ka seedha record nahi mila."})
#     except FileNotFoundError:
#         return json.dumps(
#             {"message": "Citizen requests ka data abhi available nahi hai."}
#         )
#     except Exception:
#         return json.dumps({"message": "Kuch masla aaya hai, dobara koshish karein."})


# # ------------ Tool 3: Isolation Wards (from PDF) ------------
# @function_tool
# def get_isolation_wards(province: str) -> str:
#     try:
#         wards = []
#         with pdfplumber.open(
#             "List-of-Province-wise-COVID-19-Hospital-Isolation-Wards-Pakistan.pdf"
#         ) as pdf:
#             for page in pdf.pages:
#                 text = page.extract_text()
#                 if province.lower() in text.lower():
#                     lines = text.split("\n")
#                     for line in lines:
#                         if any(
#                             word in line
#                             for word in [
#                                 "Hospital",
#                                 "Institute",
#                                 "Medical",
#                                 "Civil",
#                                 "DHQ",
#                                 "THQ",
#                             ]
#                         ):
#                             wards.append(line.strip())
#         if wards:
#             return json.dumps(wards, indent=2)
#         else:
#             return json.dumps(
#                 {"message": f"{province} ke isolation ward ka record nahi mila."}
#             )
#     except FileNotFoundError:
#         return json.dumps(
#             {"message": "Isolation wards ka data abhi available nahi hai."}
#         )
#     except Exception:
#         return json.dumps({"message": "Kuch masla aaya hai, dobara koshish karein."})


# # ------------ AGENT SETUP ------------
# Guidance_Agent: Agent = Agent(
#     name="Guidance_Agent",
#     instructions=(
#         """
# Guidance Agent Rules:

# 1. If the user mentions a city:
#     - Call `get_hospital_by_city(city)`
#     - Show hospital results to the user

# 2. If the user mentions illness, medical need, or service:
#     - Call `match_request_to_service(request)`
#     - Show the matched service details to the user

# 3. If the user asks about isolation wards:
#     - If city is provided:
#         - Call `get_hospital_by_city(city)` first
#     - If city is not provided but province is mentioned:
#         - Call `get_isolation_wards(province)`
#         - Show isolation ward list to the user
#     - If neither city nor province is mentioned:
#         - Ask user for province

# 4. If CSV or PDF files are missing:
#     - Show friendly message:
#         - "Hospital data is not available. Please provide province to get isolation wards."
#         - "Isolation ward data is not available right now."

# 5. Always respond in English
# 6. Never say: "I don’t know" or "please provide city"
# 7. Always try to give some actionable info to the user
# """
#     ),
#     model=model,
#     tools=[get_hospital_by_city, match_request_to_service, get_isolation_wards],
# )


# # ------------ MAIN RUNNER ------------
# async def main():
#     user_query = " karachi"
#     result = await Runner.run(
#         Guidance_Agent,
#         user_query,
#         run_config=config,
#     )
#     print("\n🟢 Final Agent Output:")
#     print(result.final_output)


# if __name__ == "__main__":
#     asyncio.run(main())