# 🛰️ CosmicPulse AI — Real-Time Space Intelligence Dashboard

![Python](https://img.shields.io/badge/Python-3.14-blue?style=flat-square&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.56-red?style=flat-square&logo=streamlit)
![Gemini](https://img.shields.io/badge/Google-Gemini_2.0-orange?style=flat-square&logo=google)
![Groq](https://img.shields.io/badge/Groq-LLaMA_3.3-purple?style=flat-square)

---

## 🌌 Overview

**CosmicPulse AI** is a full-stack AI-powered space intelligence dashboard that combines real-time orbital physics, live space news, and conversational AI into a single, elegant web application. Built with Python and Streamlit, it leverages cutting-edge large language models and satellite tracking to deliver a mission-control-style experience directly in your browser.

This project was built as a personal portfolio project to demonstrate practical AI/ML engineering skills including API integration, real-time data processing, and building production-ready AI applications.

---

## 🚀 Features

### 🌍 Real-Time ISS Orbit Simulation
- Tracks the International Space Station (ISS) in real time using **TLE (Two-Line Element)** data fetched live from Celestrak
- Predicts the ISS ground track for the next **60 minutes** using the **SGP4 orbital propagation model** via the Skyfield library
- Renders an interactive **dark-themed world map** using Plotly, with the ISS path overlaid as red cross markers
- Displays raw telemetry data (latitude, longitude, time) in a live-updating dataframe

### 📢 AI Mission Briefing (Live Heroic Update)
- Fetches the **latest spaceflight news articles** from the SpaceFlight News API in real time
- Passes the articles to **Groq's LLaMA 3.3 70B** model with a dramatic prompt engineering template
- Generates an inspiring, cinematic "Commander's Report" summarizing the state of humanity's space exploration
- One-click generation with a live spinner for a polished UX

### 💬 CosmicPulse Chatbot
- A fully conversational space chatbot powered by **Groq's LLaMA 3.3 70B Versatile** model
- Maintains **full conversation history** using Streamlit session state for a natural multi-turn chat experience
- Can answer any question about space, astronomy, physics, missions, black holes, exoplanets, and more
- Designed to be engaging, accurate, and inspiring

### 📐 Technical Details Tab
- Dedicated tab explaining the orbital mechanics behind the ISS altitude calculation
- Renders the formula: **h = r − Rₑ** using LaTeX math rendering in Streamlit
- Explains SGP4 propagation, TLE data, atmospheric drag, and gravitational perturbations

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit |
| Orbital Physics | Skyfield, SGP4 |
| LLM (Chatbot + News) | Groq — LLaMA 3.3 70B |
| LLM (Knowledge Agent) | Google Gemini 2.0 Flash |
| News API | SpaceFlight News API |
| Data Visualization | Plotly Express |
| Data Processing | Pandas, NumPy |
| Environment Management | python-dotenv |

---

## 📁 Project Structure
