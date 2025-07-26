from google.adk.agents import Agent
import requests

GEMINI_MODEL = "gemini-2.0-flash"
GOOGLE_API_KEY = "AIzaSyCgedouy--s0p5obD4jVSDKKZ9RyYPAfn0"

def get_google_maps_url(origin_lat, origin_lng, dest_lat, dest_lng) -> str:
    """
    Returns a Google Maps navigation URL from origin to destination.
    """
    return (
        f"https://www.google.com/maps/dir/?api=1"
        f"&origin={origin_lat},{origin_lng}"
        f"&destination={dest_lat},{dest_lng}"
        f"&travelmode=driving"
    )

def get_directions(origin_lat, origin_lng, dest_lat, dest_lng, api_key=GOOGLE_API_KEY) -> str:
    """
    Uses Google Directions API to get navigation details from origin to destination.
    """
    url = "https://maps.googleapis.com/maps/api/directions/json"
    params = {
        "origin": f"{origin_lat},{origin_lng}",
        "destination": f"{dest_lat},{dest_lng}",
        "key": api_key,
        "mode": "driving"  # or "walking", "bicycling", "transit"
    }
    response = requests.get(url, params=params)
    data = response.json()
    if data.get("status") != "OK":
        return f"Error fetching directions: {data.get('status')}"
    steps = data["routes"][0]["legs"][0]["steps"]
    directions = []
    for step in steps:
        import re
        instruction = re.sub('<[^<]+?>', '', step["html_instructions"])
        distance = step["distance"]["text"]
        directions.append(f"{instruction} ({distance})")
        maps_url = get_google_maps_url(origin_lat, origin_lng, dest_lat, dest_lng)
    return "\n".join(directions) + f"\n\n[Open in Google Maps]({maps_url})"

def navigation_tool(origin_lat: float, origin_lng: float, dest_lat: float, dest_lng: float) -> str:
    return get_directions(origin_lat, origin_lng, dest_lat, dest_lng)

navigation_agent = Agent(
    name="NavigationAgent",
    model=GEMINI_MODEL,
    instruction="""
    You are a helpful assistant that can use the following tool:
    - Find the navigation root based on the origin_lat = latitude and origin_lng = longitude from {current_location} as origin and the 1st hospital latitude and longitude as destination:
    - navigation_tool
    """,
    tools=[navigation_tool],
    description="Get navigation directions from one location to another.",
)