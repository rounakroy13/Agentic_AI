"""
Emergency Agent Chat Application
--------------------------------
Provides a chat interface for interacting with the Emergency Manager Agent.
Allows users to create sessions, send messages, and receive responses from the ADK API.

Requirements:
- ADK API Server running on localhost:8000
- Emergency Manager Agent registered in the ADK
"""

import streamlit as st
import requests
import json
import os
import uuid
import time

# Streamlit page settings
st.set_page_config(page_title="Emergency Chat", page_icon="🚑", layout="centered")

# Constants
API_BASE_URL = "http://localhost:8000"  # ADK API Server
APP_NAME = "emergency_manager"          # Your root agent name

# Session State
if "user_id" not in st.session_state:
    st.session_state.user_id = f"user-{uuid.uuid4()}"

if "session_id" not in st.session_state:
    st.session_state.session_id = None

if "messages" not in st.session_state:
    st.session_state.messages = []

# Functions
def create_session():
    """Create a new session with the emergency agent."""
    session_id = f"session-{int(time.time())}"
    response = requests.post(
        f"{API_BASE_URL}/apps/{APP_NAME}/users/{st.session_state.user_id}/sessions/{session_id}",
        headers={"Content-Type": "application/json"},
        data=json.dumps({})
    )
    if response.status_code == 200:
        st.session_state.session_id = session_id
        st.session_state.messages = []
        return True
    else:
        st.error(f"Failed to create session: {response.text}")
        return False

def send_message(message: str):
    """Send a message to the Emergency Agent and process the response."""
    if not st.session_state.session_id:
        st.error("No active session. Please create a session first.")
        return False

    # Add user message
    st.session_state.messages.append({"role": "user", "content": message})

    # Send message to ADK API
    response = requests.post(
        f"{API_BASE_URL}/run",
        headers={"Content-Type": "application/json"},
        data=json.dumps({
            "app_name": APP_NAME,
            "user_id": st.session_state.user_id,
            "session_id": st.session_state.session_id,
            "new_message": {
                "role": "user",
                "parts": [{"text": message}]
            }
        })
    )

    if response.status_code != 200:
        st.error(f"Error: {response.text}")
        return False

    # Process ADK response
    events = response.json()
    assistant_message = None

    for event in events:
        content = event.get("content", {})
        if content.get("role") == "model" and "parts" in content:
            for part in content["parts"]:
                if "text" in part:
                    assistant_message = part["text"]

    if assistant_message:
        st.session_state.messages.append({"role": "assistant", "content": assistant_message})

    return True

# UI Components
st.title("🚑 Emergency Chatbot")

# Sidebar: Session management
with st.sidebar:
    st.header("Session Management")
    if st.session_state.session_id:
        st.success(f"Active session: {st.session_state.session_id}")
        if st.button("➕ New Session"):
            create_session()
    else:
        st.warning("No active session")
        if st.button("➕ Create Session"):
            create_session()

    st.divider()
    st.caption("Ensure ADK API Server is running at port 8000.")

# Chat interface
st.subheader("Chat with Emergency Agent")

# Display messages
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])
    else:
        st.chat_message("assistant").write(msg["content"])

# Input for new messages
if st.session_state.session_id:
    user_input = st.chat_input("Describe your emergency...")
    if user_input:
        send_message(user_input)
        st.rerun()
else:
    st.info("👈 Create a session to start chatting.")
