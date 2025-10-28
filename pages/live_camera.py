import streamlit as st

st.set_page_config(page_title="Live Camera - AI Parking", layout="wide")

st.markdown("""
    <style>
    .main-title {
        font-size: 36px;
        color: #00FFD1;
        text-align: center;
        font-weight: bold;
        margin-top: 20px;
    }
    .tagline {
        text-align: center;
        color: #B0B0B0;
        font-size: 18px;
        margin-bottom: 20px;
    }
    .stApp {
        background-color: #0E1117;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🎥 Live Camera Parking Detection</div>', unsafe_allow_html=True)
st.markdown('<div class="tagline">Use your webcam to monitor parking space occupancy in real time 🚗</div>', unsafe_allow_html=True)

# Live camera input
frame = st.camera_input("Activate Camera to Detect Parking Spaces")

if frame:
    st.success("✅ Camera active! Processing frame...")

    # You can later add YOLO or OpenCV model inference here
    st.image(frame, caption="Captured Frame", use_container_width=True)

    st.info("🧠 In future: This frame can be analyzed using your YOLO model to detect empty/occupied slots.")
