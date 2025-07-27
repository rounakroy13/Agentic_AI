# Civic Lens AI - Sequential Agent

This project demonstrates a modular, agentic AI pipeline for emergency support and civic assistance using the Google Agent Development Kit (ADK).

## Features

- **Location Detection:** Fetches the user's current location (via IP).
- **Hospital Finder:** Finds the nearest hospitals using Google Places API.
- **Ambulance Recommender:** Recommends the nearest ambulance service.
- **Navigation:** Provides directions and Google Maps links from the user's location to the hospital.
- **Notification:** Sends notifications (e.g., SMS via Twilio) to users or admins.
- **Voice Command Trigger:** (Optional) Supports triggering the pipeline via voice command.

## Directory Structure

```
sequential-agent/
├── src/
│   └── subagents/
│       ├── hospital/
│       │   └── agent.py
│       ├── navigation/
│       │   └── agent.py
│       ├── notification/
│       │   └── agent.py
│       ├── recommender/
│       │   └── agent.py
│       └── validator/
│           └── agent.py
├── agent.py
└── README.md
```

## Setup

1. **Clone the repository and navigate to the project directory.**

2. **Create and activate a virtual environment:**
   ```sh
   python -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

4. **Set up API keys:**
   - Google Places API (for hospital/ambulance/navigation)
   - Twilio (for SMS notifications)
   - You can set these as environment variables or directly in the code (not recommended for production).

## Running the Agent

Run the main agent pipeline:
```sh
python src/agent.py
```

Or run/test individual subagents as needed.

## Customization

- **Add new subagents** by creating a new folder in `src/subagents/` and registering it in the main pipeline.
- **Integrate with other notification services** (email, Slack, etc.) by modifying `notification/agent.py`.

## Notes

- The current location is approximate (IP-based). For GPS, use a mobile app or browser integration.
- Voice command support requires additional setup (see code comments).
- Do not use YAML configs with ADK; use Python-based agent definitions.

## License

MIT License

---

**For questions or contributions, please open an issue or pull request.**