from google.adk.agents import Agent
from twilio.rest import Client
import os

# Set your Twilio credentials (use environment variables for security)
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "ACb03f56517f84e7769b7d8da41c6cd9a4")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "9920dc71707fbd22be785e42e1945579")

def send_sms_notification(message: str, to_number: str) -> str:
    """
    Sends an SMS notification using Twilio.
    """
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        sms = client.messages.create(
            body=message,
            from_='+919051167655',
            to='+918013257020'
        )
        return f"SMS sent to {to_number}: SID {sms.sid}"
    except Exception as e:
        return f"Failed to send SMS: {e}"

notification_agent = Agent(
    name="NotificationAgent",
    model="gemini-1.5-pro",
    instruction="""
    You are a helpful assistant that can use the following tool:
    - send_sms_notification
    - message: {Emergency Support needed ! ! !}
    """,
    tools=[send_sms_notification],
    description="Agent to send SMS notifications using Twilio.",
)