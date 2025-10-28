import streamlit as st
from ultralytics import YOLO
from PIL import Image

# Page title
st.title("🚘 Parking Spot Detection")

# Load your trained YOLO model
model_path = "C:/Users/legen/runs/detect/train8/weights/best.pt"
model = YOLO(model_path)

# File uploader
uploaded_file = st.file_uploader("Upload a parking lot image", type=["jpg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)

    with st.spinner("Detecting parking spaces..."):
        results = model.predict(image)

    # Display results
    result_image = results[0].plot()
    st.image(result_image, caption="Detected Parking Slots", use_container_width=True)

    # Optional: show number of slots detected
    boxes = results[0].boxes
    empty_slots = sum(1 for cls in boxes.cls if cls == 0)
    occupied_slots = sum(1 for cls in boxes.cls if cls == 1)

    st.success(f"✅ Empty Slots: {empty_slots} | 🚗 Occupied Slots: {occupied_slots}")
