"""
Sequential Agent to beloow task

If asked about emergency support
fetch curent location as latitude and longitude
Then use latitude and longitude to find nearest hospitals
"""

from google.adk.agents import SequentialAgent
from .subagents.recommender import action_recommender_agent
from .subagents.hospital import fetch_hospital
from .subagents.navigation import navigation_agent
from .subagents.location import fetch_location_agent

root_agent = SequentialAgent(
    name="LeadQualificationPipeline",
    sub_agents=[fetch_location_agent, fetch_hospital, action_recommender_agent, navigation_agent],
    description="A pipeline that validates, scores, and recommends actions for sales leads",
)
