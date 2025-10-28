import streamlit as st
from streamlit_folium import st_folium
import folium

# -------------------- PAGE CONFIG --------------------
st.set_page_config(page_title="AI Parking & EV Assistant", layout="wide")

# -------------------- CUSTOM CSS --------------------
st.markdown("""
    <style>
    .main-title {
        font-size: 45px;
        color: #00FFD1;
        text-align: center;
        font-weight: bold;
        margin-top: 10px;
    }
    .tagline {
        text-align: center;
        color: #B0B0B0;
        font-size: 18px;
        margin-bottom: 40px;
    }
    .center-buttons {
        display: flex;
        justify-content: center;
        gap: 25px;
        margin-top: 20px;
        margin-bottom: 40px;
    }
    button[data-baseweb="button"] {
        background-color: #00FFD1 !important;
        color: black !important;
        font-weight: bold;
        border-radius: 12px !important;
        padding: 0.6em 2em !important;
        transition: 0.3s ease;
    }
    button[data-baseweb="button"]:hover {
        transform: scale(1.05);
        background-color: #00e6b8 !important;
    }
    .stApp {
        background-color: #0E1117;
    }
    hr {
        border: 1px solid #333;
        margin-top: 10px;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# -------------------- HEADER --------------------
st.markdown('<div class="main-title">🚗 AI Parking & EV Assistant</div>', unsafe_allow_html=True)
st.markdown('<div class="tagline">Smart Parking & EV Charging Recommendations Powered by AI ⚡</div>', unsafe_allow_html=True)

# -------------------- BUTTONS --------------------
st.markdown('<div class="center-buttons">', unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    if st.button("🔍 Detect Parking Spots"):
        st.switch_page("pages/detect_parking.py")

with col2:
    if st.button("⚡ Find Charging Stations"):
        st.switch_page("pages/charging_stations.py")

with col3:
    if st.button("🎥 Live Camera View"):
        st.switch_page("pages/live_camera.py")  # optional, if you later add camera page

st.markdown('</div>', unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

# -------------------- LARGE MAP SECTION --------------------
st.markdown("### 🌍 Explore Nearby Parking & Charging Zones")

# Create a large map with Thane as default location
m = folium.Map(location=[19.2183, 72.9781], zoom_start=12, control_scale=True)

# Example markers (you can add dynamically later)
folium.Marker(
    [19.2183, 72.9781],
    popup="Thane Parking Area 🅿️",
    tooltip="Parking Spot",
    icon=folium.Icon(color="green", icon="car", prefix="fa")
).add_to(m)

folium.Marker(
    [19.23, 72.97],
    popup="EV Charging Station ⚡",
    tooltip="Charging Station",
    icon=folium.Icon(color="blue", icon="bolt", prefix="fa")
).add_to(m)

folium.Marker(
    [19.21, 72.99],
    popup="Parking + Charging Combo 🚗⚡",
    tooltip="Combo Spot",
    icon=folium.Icon(color="purple", icon="charging-station", prefix="fa")
).add_to(m)

# -------------------- DISPLAY MAP --------------------
st_folium(m, width=1500, height=750)
