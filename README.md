# CosmicPulse AI Space Command

CosmicPulse is a Streamlit web app that combines live space news, ISS orbit visualization, and a conversational space assistant.

## Essential Features

- Mission Briefing: Generates a concise live space-news update.
- Real-Time Orbit Simulation: Shows ISS trajectory on an interactive 3D globe.
- Technical View: Displays predicted ISS latitude/longitude data and orbital explanation.
- Space Chatbot: Answers user questions about space, astronomy, and missions.

## Tech Stack

- Python
- Streamlit
- Skyfield
- Globe.gl (via Streamlit HTML component)
- Groq API

## Run Locally

1. Create and activate a virtual environment.
2. Install dependencies:
   - `pip install -r requirements.txt` (if available), or install required packages manually.
3. Add your API keys to `keys.env` (kept local and ignored by git).
4. Start the app:
   - `streamlit run app.py`
