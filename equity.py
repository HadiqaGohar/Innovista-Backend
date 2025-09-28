# import asyncio
# import os
# import json
# from typing import List, Dict, Tuple
# from dotenv import load_dotenv

# import camelot
# import pandas as pd
# import googlemaps
# from geopy.distance import geodesic

# from agents import Agent, OpenAIChatCompletionsModel, Runner, RunConfig, AsyncOpenAI, ModelSettings, function_tool

# load_dotenv()


# # -------------------------------
# # Google Maps Service
# # -------------------------------
# class GoogleMapsService:
#     def __init__(self):
#         self.api_key = os.getenv("GOOGLE_MAPS_API_KEY")
#         if not self.api_key:
#             raise ValueError("GOOGLE_MAPS_API_KEY environment variable is not set")
#         self.gmaps = googlemaps.Client(key=self.api_key)
#         self.geocode_cache = {}

#     def geocode_location(self, location_text: str, location_type: str = "general") -> Tuple[float, float]:
#         if location_text in self.geocode_cache:
#             return self.geocode_cache[location_text]

#         try:
#             query = f"{location_text}, Pakistan"
#             if location_type == "hospital":
#                 query = f"{location_text}, hospital, Pakistan"
#             result = self.gmaps.geocode(query)
#             if result:
#                 loc = result[0]['geometry']['location']
#                 coords = (loc['lat'], loc['lng'])
#                 self.geocode_cache[location_text] = coords
#                 return coords
#         except Exception as e:
#             print(f"Geocoding failed for '{location_text}': {str(e)}")
#         return (0.0, 0.0)

#     def calculate_travel_distances(self, origin: Tuple[float, float], destinations: List[Tuple[float, float]]) -> List[Dict]:
#         try:
#             if not destinations:
#                 return []
#             matrix = self.gmaps.distance_matrix(origins=[origin], destinations=destinations, mode="driving", units="metric", departure_time="now")
#             elements = matrix['rows'][0]['elements']
#             results = []
#             for idx, element in enumerate(elements):
#                 if element['status'] == 'OK':
#                     dist_km = element['distance']['value'] / 1000
#                     dur_min = element['duration']['value'] / 60
#                     dur_traffic = element.get('duration_in_traffic', {}).get('value', element['duration']['value']) / 60
#                     results.append({'index': idx, 'distance_km': round(dist_km,2), 'duration_minutes': round(dur_min,1), 'duration_in_traffic_minutes': round(dur_traffic,1), 'status': 'SUCCESS'})
#                 else:
#                     results.append({'index': idx, 'distance_km': None, 'duration_minutes': None, 'duration_in_traffic_minutes': None, 'status': f"FAILED - {element['status']}"})
#             return results
#         except Exception as e:
#             print(f"Distance Matrix API error: {str(e)}")
#             return []

#     def validate_hospital_location(self, hospital_name: str, district: str) -> Dict:
#         try:
#             query = f"{hospital_name} hospital {district} Pakistan"
#             result = self.gmaps.places(query=query, type='hospital')
#             if result['status'] == 'OK' and result['results']:
#                 place = result['results'][0]
#                 loc = place['geometry']['location']
#                 return {
#                     'validated': True, 'lat': loc['lat'], 'lng': loc['lng'],
#                     'place_id': place.get('place_id', ''), 'formatted_address': place.get('formatted_address', ''),
#                     'rating': place.get('rating', 0), 'types': place.get('types', [])
#                 }
#             lat, lng = self.geocode_location(f"{hospital_name}, {district}", "hospital")
#             return {'validated': lat!=0.0 and lng!=0.0, 'lat': lat, 'lng': lng, 'place_id': '', 'formatted_address': f"{hospital_name}, {district}, Pakistan", 'rating': 0, 'types': ['hospital']}
#         except Exception as e:
#             print(f"Hospital validation failed for {hospital_name}: {str(e)}")
#             return {'validated': False, 'lat':0.0, 'lng':0.0, 'place_id':'', 'formatted_address':'', 'rating':0, 'types':[]}


# _maps_service = GoogleMapsService()


# # -------------------------------
# # Tools
# # -------------------------------
# @function_tool
# def load_citizen_requests(file_path: str):
#     try:
#         if not os.path.exists(file_path):
#             raise FileNotFoundError(f"Citizen requests file not found: {file_path}")
#         with open(file_path, "r", encoding="utf-8") as f:
#             raw_data = json.load(f)
#         if not isinstance(raw_data, list):
#             raise ValueError("Expected a list of requests")
#         validated_requests = []
#         for idx, request in enumerate(raw_data):
#             val = _validate_request_structure(request, idx)
#             if val["is_valid"]:
#                 validated_requests.append(val["request"])
#         return validated_requests
#     except Exception as e:
#         return {"error": str(e), "requests": [], "status":"FAILED"}

# def _validate_request_structure(request, index):
#     try:
#         if not isinstance(request, dict): return {"is_valid":False,"error":f"Request {index} invalid","request":None}
#         profile = request.get("citizen_profile", {})
#         if not all(profile.get(f) for f in ["full_name","location"]):
#             return {"is_valid":False,"error":f"Request {index} missing profile fields","request":None}
#         return {"is_valid":True,"error":None,"request":{
#             "case_id": request.get("case_id", f"UNKNOWN-{index}"),
#             "citizen_id": request.get("citizen_id", f"CITIZEN-{index}"),
#             "request_type": request.get("request_type", "Healthcare Request"),
#             "timestamp": request.get("timestamp", ""),
#             "citizen_profile": {
#                 "full_name": profile["full_name"].strip(),
#                 "age": profile.get("age", 0),
#                 "location": profile["location"].strip(),
#                 "contact_info": profile.get("contact_info", {})
#             }
#         }}

# @function_tool
# def validate_hospital_locations_tool(hospitals_data: str) -> str:
#     try:
#         hospitals_list = json.loads(hospitals_data)
#         validated_hospitals = []
#         for hospital in hospitals_list:
#             name, district = hospital.get('Hospital',''), hospital.get('District','')
#             validation = _maps_service.validate_hospital_location(name,district)
#             hospital.update({
#                 'lat': validation['lat'],
#                 'lng': validation['lng'],
#                 'validated_location': validation['validated'],
#                 'formatted_address': validation['formatted_address'],
#                 'place_id': validation['place_id'],
#                 'google_rating': validation['rating'],
#                 'place_types': validation['types'],
#                 'validation_status': 'SUCCESS' if validation['validated'] else 'FAILED'
#             })
#             validated_hospitals.append(hospital)
#         return json.dumps({"validated_hospitals": validated_hospitals, "status":"SUCCESS"})
#     except Exception as e:
#         return json.dumps({"error": str(e), "status":"FAILED"})

# @function_tool
# def google_maps_distance_tool(citizen_location: str, hospitals_data: str) -> str:
#     try:
#         hospitals_list = json.loads(hospitals_data)
#         citizen_coords = _maps_service.geocode_location(citizen_location, "citizen")
#         hospital_coords = [(h.get('lat',0.0), h.get('lng',0.0)) for h in hospitals_list if h.get('Beds',0)>0]
#         distances = _maps_service.calculate_travel_distances(citizen_coords, hospital_coords)
#         enhanced = []
#         for i,h in enumerate(hospitals_list):
#             if i < len(distances):
#                 h.update({
#                     'citizen_coordinates': citizen_coords,
#                     'hospital_coordinates': (h.get('lat',0.0), h.get('lng',0.0)),
#                     'travel_distance_km': distances[i]['distance_km'],
#                     'travel_time_minutes': distances[i]['duration_minutes'],
#                     'travel_time_with_traffic_minutes': distances[i]['duration_in_traffic_minutes'],
#                     'assignment_status': 'AVAILABLE'
#                 })
#                 enhanced.append(h)
#         enhanced.sort(key=lambda x: x.get('travel_time_minutes', float('inf')))
#         return json.dumps({"hospitals_with_distances":enhanced, "citizen_location":citizen_location, "status":"SUCCESS"})
#     except Exception as e:
#         return json.dumps({"error": str(e), "citizen_location": citizen_location, "status":"FAILED"})


# # -------------------------------
# # Hospital PDF Loading
# # -------------------------------
# def load_hospitals_from_pdf(pdf_path: str):
#     tables = camelot.read_pdf(pdf_path, pages='all', flavor='stream')
#     hospitals = []
#     for table in tables:
#         df = table.df
#         for i,row in df.iterrows():
#             row_vals = [str(v).strip() for v in row.values if str(v).strip()]
#             if len(row_vals)>=3:
#                 try:
#                     beds = float(row_vals[-1])
#                     hospital = row_vals[2] if len(row_vals)>=4 else row_vals[1]
#                     district = row_vals[1] if len(row_vals)>=4 else "Unknown"
#                     hospitals.append({'Sr': row_vals[0],'District':district,'Hospital':hospital,'Beds':beds})
#                 except: continue
#     df = pd.DataFrame(hospitals)
#     df = add_hospital_coordinates(df)
#     return df

# def add_hospital_coordinates(df: pd.DataFrame):
#     gmaps_key = os.getenv("GOOGLE_MAPS_API_KEY")
#     if not gmaps_key: return df
#     gmaps = googlemaps.Client(key=gmaps_key)
#     for idx,row in df.iterrows():
#         try:
#             query = f"{row['Hospital']}, {row['District']}, Pakistan"
#             res = gmaps.geocode(query)
#             if res:
#                 loc = res[0]['geometry']['location']
#                 df.at[idx,'lat']=loc['lat']; df.at[idx,'lng']=loc['lng']
#         except: continue
#     return df


# # -------------------------------
# # Hospital Assignment Tool
# # -------------------------------
# @function_tool
# def hospital_assignment_tool(pdf_path: str, json_path: str):
#     try:
#         hospitals_df = load_hospitals_from_pdf(pdf_path)
#         citizen_requests = load_citizen_requests(json_path)
#         assignments = []
#         for req in citizen_requests:
#             citizen_loc = req.get("citizen_profile",{}).get("location","")
#             distances = google_maps_distance_tool(citizen_loc, hospitals_df.to_json(orient='records'))
#             assignments.append(json.loads(distances))
#         return {"assignments": assignments, "status":"SUCCESS"}
#     except Exception as e:
#         return {"error": str(e), "assignments": [], "status":"FAILED"}


# # -------------------------------
# # Main Agent
# # -------------------------------
# async def main():
#     GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
#     if not GEMINI_API_KEY: raise ValueError("GEMINI_API_KEY not set")

#     client = AsyncOpenAI(api_key=GEMINI_API_KEY, base_url="https://generativelanguage.googleapis.com/v1beta/openai/")
#     gemini_model = OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client)
#     config = RunConfig(model=gemini_model, model_provider=client, tracing_disabled=True)

#     equity_agent = Agent(
#         name="Equity Oversight Agent",
#         instructions="""
# You are an elite AI Equity Oversight Agent specializing in healthcare resource allocation and equity analysis.
#         """,
#         tools=[load_citizen_requests, hospital_assignment_tool, google_maps_distance_tool, validate_hospital_locations_tool],
#         model_settings=ModelSettings(tool_choice="required")
#     )

#     result = await Runner.run(
#         starting_agent=equity_agent,
#         input="Load citizen requests and hospital data, analyze hospital assignments, and provide an executive summary.",
#         run_config=config
#     )
#     print(result.final_output)


# if __name__ == "__main__":
#     asyncio.run(main())