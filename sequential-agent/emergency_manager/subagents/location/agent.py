"""
location Agent

This agent is responsible for validating if a lead has all the necessary information
for qualification.
"""

from google.adk.agents import Agent
import requests

GEMINI_MODEL = "gemini-2.0-flash"

def get_current_location() -> dict:
    response = requests.get("https://ipinfo.io/json")
    data = response.json()
    loc = data.get("loc", "")
    if loc:
        latitude, longitude = map(float, loc.split(","))
        return {
            "latitude": latitude,
            "longitude": longitude
        }

fetch_location_agent = Agent(
    name="LocationAgent",
    model=GEMINI_MODEL,
    instruction="""
    If asked about emergency health supoort
    You are a helpful assistant that can use the following tools:
    get current location as latitude and longitude.

    Output should have latitude and longitude value.
    """,
    tools=[get_current_location],
    output_key="current_location"
)
