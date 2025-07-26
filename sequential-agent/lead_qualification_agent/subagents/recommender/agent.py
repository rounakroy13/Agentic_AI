"""
Action Recommender Agent

This agent is responsible for recommending appropriate next actions
based on the lead validation and scoring results.
"""

from google.adk.agents import Agent
import requests

# --- Constants ---
GEMINI_MODEL = "gemini-2.0-flash"

def find_nearest_ambulance(latitude: float, longitude: float, api_key: str, radius: int = 3000) -> str:
    """
    Uses Google Places API to find nearby ambulance.
    """
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        "key": api_key,
        "location": f"{latitude},{longitude}",
        "radius": radius,
        "type": "hospital",
        "keyword": "ambulance"
    }
    response = requests.get(url, params=params)
    data = response.json()
    if data.get("status") != "OK":
        return f"Error fetching data: {data.get('status')}"
    ambulance = data.get("results", [])[0]
    result = []
    name = ambulance.get("name")
    address = ambulance.get("vicinity")
    rating = ambulance.get("rating", "N/A")
    result.append(f"🏥 {name} — {address} (⭐ {rating})")
    return "\n".join(result) if result else "No ambulance found nearby."

# Replace with your actual Google Places API key
GOOGLE_API_KEY = "AIzaSyCgedouy--s0p5obD4jVSDKKZ9RyYPAfn0"

def ambulance_tool(latitude: float, longitude: float) -> str:
    return find_nearest_ambulance(latitude, longitude, GOOGLE_API_KEY)

# Create the recommender agent
action_recommender_agent = Agent(
     name="HospitalAgent",
    model=GEMINI_MODEL,

    instruction="""
    You are a helpful assistant that can use the following tools:
    Find the nearest ambulance based on the latitude and longitude provided:
    - use latututde and longitude from {current_location}

    Output should have top 1 ambulance service with contact details and  information
    """,
    tools=[ambulance_tool],

    description="Find nearest Ambulance Service",
)
