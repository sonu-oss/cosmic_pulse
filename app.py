import streamlit as st
import pandas as pd
from data_engine import fetch_latest_spaceflight_news_articles, summarize_articles_to_heroic_update
from orbit_engine import get_iss_prediction
from cosmic_agent import ask_free_chatbot
from globe_components.globe_component import render_satellite_globe

# --- Page Config ---
st.set_page_config(
    page_title="CosmicPulse AI",
    layout="wide",
    page_icon="🚀",
    initial_sidebar_state="collapsed",
)

# --- Custom Styling ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .main { background-color: #0b0d17; color: #eef3ff; }
    h1, h2, h3 {
        font-family: 'Space Grotesk', sans-serif;
        letter-spacing: 0.2px;
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        border: 1px solid #2f4375;
        background: linear-gradient(135deg, #1f4b99 0%, #3769c9 100%);
        color: #f8fbff;
        font-weight: 600;
    }
    .stButton>button:hover {
        border-color: #4f74cc;
        background: linear-gradient(135deg, #2a58ac 0%, #4478db 100%);
    }
    [data-testid="stSidebar"] { display: none; }
    [data-testid="collapsedControl"] { display: none; }
    </style>
    """, unsafe_allow_html=True)

st.title("CosmicPulse: AI Space Command")
st.caption("Powered by Gemini 2.0 Flash and Orbital Physics")

# --- Layout ---
col_left, col_right = st.columns([1, 1.2])

with col_left:
    st.header("Mission Briefing")
    if st.button("Generate Live Heroic Update"):
        with st.spinner("Gemini is interpreting the signals..."):
            raw_news = fetch_latest_spaceflight_news_articles()
            summary = summarize_articles_to_heroic_update(raw_news)
            st.markdown(f"### Commander's Report\n{summary}")

with col_right:
    st.header("Real-Time Orbit Simulation")
    tab1, tab2 = st.tabs(["Orbit Map", "Technical Details"])

    with tab1:
        with st.expander("Why this matters?"):
            st.write("Using SGP4 Propagator models to predict the path of the ISS for the next 60 minutes.")

        orbit_data = get_iss_prediction(minutes_ahead=60)
        df = pd.DataFrame(orbit_data)
        if orbit_data:
            current = orbit_data[0]
            satellites = [
                {
                    "name": "ISS",
                    "lat": current["lat"],
                    "lon": current["lon"],
                    "alt_km": 408,
                    "color": "#55d6ff",
                }
            ]
            ground_tracks = [
                {
                    "name": "ISS",
                    "points": [(p["lat"], p["lon"]) for p in orbit_data],
                    "color": "#55d6ff",
                    "alt_km": 408,
                }
            ]
            render_satellite_globe(
                satellites=satellites,
                ground_tracks=ground_tracks,
                height=520,
                auto_rotate=True,
                accent_color="#55d6ff",
            )
        st.dataframe(df.style.highlight_max(axis=0), use_container_width=True)

    with tab2:
        st.subheader("Orbital Mechanics: Altitude Calculation")
        st.markdown("""
        The ISS altitude $h$ is derived from:
        $$h = r - R_e$$
        Where:
        - $r$ = orbital radius from Earth's center (km)
        - $R_e$ = Earth's mean radius = **6,371 km**

        The **SGP4 model** propagates the ISS position using TLE (Two-Line Element) data,
        accounting for atmospheric drag, gravitational harmonics, and solar radiation pressure.
        The result is a predicted ground track updated every 5 minutes.
        """)

st.divider()

# --- Chatbot ---
st.header("CosmicPulse Chatbot")
st.caption("Ask me anything about space, astronomy, or the universe!")

if "chatbot_history" not in st.session_state:
    st.session_state.chatbot_history = []

for msg in st.session_state.chatbot_history:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

user_input = st.chat_input("Ask about black holes, Mars, JWST, anything...")
if user_input:
    st.session_state.chatbot_history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            reply = ask_free_chatbot(st.session_state.chatbot_history)
            st.write(reply)
            st.session_state.chatbot_history.append({"role": "assistant", "content": reply})

st.divider()
st.markdown(
    "<p style='text-align:center; color:gray;'>Built for the Google AI Hackathon 2026</p>",
    unsafe_allow_html=True,
)
