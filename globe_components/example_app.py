"""
Example Streamlit app showing how to use globe_component.py
-----------------------------------------------------------
Run:
    pip install streamlit requests
    streamlit run example_app.py
"""
import math
import time
from datetime import datetime, timezone

import requests
import streamlit as st

from globe_component import render_satellite_globe

st.set_page_config(page_title="Orbital Tracker", layout="wide")

st.markdown(
    """
    <style>
      .stApp { background: #03060d; color: #d6f3ff; }
      h1, h2, h3 { color: #00e5ff; letter-spacing: .14em; text-transform: uppercase; }
      .block-container { padding-top: 1.2rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("// ORBITAL TRACKER")

# ---------- 1) live ISS position (free, no API key) -------------------------
@st.cache_data(ttl=8)
def fetch_iss():
    try:
        r = requests.get("https://api.wheretheiss.at/v1/satellites/25544", timeout=5)
        d = r.json()
        return float(d["latitude"]), float(d["longitude"]), float(d["altitude"])
    except Exception:
        return 45.51731, -40.42968, 408.0  # fallback


# ---------- 2) build a synthetic orbit path around the current position -----
def synth_groundtrack(lat0, lon0, n=140, inclination_deg=51.6):
    """Quick fake great-circle trail so the globe has a moving arc.
    Replace this with your real predicted ground-track points."""
    inc = math.radians(inclination_deg)
    pts = []
    for i in range(n):
        f = (i / n) * 2 * math.pi
        lat = math.degrees(math.asin(math.sin(inc) * math.sin(f)))
        lon = (lon0 + math.degrees(f) - 180) % 360 - 180
        pts.append((lat, lon))
    return pts


lat, lon, alt = fetch_iss()

satellites = [
    {"name": "ISS",     "lat": lat,    "lon": lon,    "alt_km": alt, "color": "#00e5ff"},
    {"name": "HUBBLE",  "lat": 12.7,   "lon":  77.5,  "alt_km": 540, "color": "#ff3df0"},
    {"name": "STARLINK","lat": -23.4,  "lon": -55.0,  "alt_km": 550, "color": "#7cff7c"},
]

ground_tracks = [
    {"name": "ISS",     "points": synth_groundtrack(lat, lon),       "color": "#00e5ff", "alt_km": alt},
    {"name": "HUBBLE",  "points": synth_groundtrack(12.7, 77.5, inclination_deg=28.5), "color": "#ff3df0", "alt_km": 540},
]

render_satellite_globe(
    satellites=satellites,
    ground_tracks=ground_tracks,
    height=720,
    auto_rotate=True,
    accent_color="#00e5ff",
)

c1, c2, c3 = st.columns(3)
c1.metric("ISS LAT",  f"{lat:.4f}°")
c2.metric("ISS LON",  f"{lon:.4f}°")
c3.metric("ALT (KM)", f"{alt:.1f}")

# auto-refresh every 8s
time.sleep(8)
st.rerun()
