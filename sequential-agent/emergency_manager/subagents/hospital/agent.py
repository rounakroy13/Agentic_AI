"""
Hospital Agent

This agent is responsible for for searching Hospitals based on the latitude and longitude provided.
It uses the Google Places API to find nearby hospitals and returns the top 3 results with details
"""

from google.adk.agents import Agent
import requests

# --- Constants ---
GEMINI_MODEL = "gemini-2.0-flash"

def find_nearest_hospitals(latitude: float, longitude: float, api_key: str, radius: int = 3000) -> str:
    """
    Uses Google Places API to find nearby hospitals.
    """
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        "key": api_key,
        "location": f"{latitude},{longitude}",
        "radius": radius,
        "type": "hospital"
    }
    response = requests.get(url, params=params)
    data = response.json()
    if data.get("status") != "OK":
        return f"Error fetching data: {data.get('status')}"
    hospitals = data.get("results", [])
    result = []
    for hospital in hospitals[:1]:
        name = hospital.get("name")
        address = hospital.get("vicinity")
        rating = hospital.get("rating", "N/A")
        result.append(f"🏥 {name} — {address} (⭐ {rating})")
    return "\n".join(result) if result else "No hospitals found nearby."

GOOGLE_API_KEY = "AIzaSyCgedouy--s0p5obD4jVSDKKZ9RyYPAfn0"

def hospital_tool(latitude: float, longitude: float) -> str:
    return find_nearest_hospitals(latitude, longitude, GOOGLE_API_KEY)

fetch_hospital = Agent(
    name="Hospital_Agent",
    model=GEMINI_MODEL,

    instruction="""
    You are a helpful assistant that can use the following tools:
    Find the nearest hospital based on the latitude and longitude provided:
    - use latututde and longitude from {current_location}

    Output should have top 3 hospital details with information
    """,
    tools=[hospital_tool],

    description="FInd nearest Hospital",
    output_key="hospital_details"
)
