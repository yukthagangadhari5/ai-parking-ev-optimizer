import streamlit as st
import folium
import requests
from streamlit_folium import st_folium
import subprocess
import sys

# --- Ensure geopy is available even if Streamlit Cloud fails to install it ---
try:
    from geopy.geocoders import Nominatim
    from geopy.distance import geodesic
except ImportError:
    st.warning("⚙️ Installing geopy module (first-time setup)... Please wait a few seconds.")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "geopy"])
    from geopy.geocoders import Nominatim
    from geopy.distance import geodesic

# --- Streamlit Page Setup ---
st.set_page_config(page_title="EV Charging Stations", page_icon="⚡", layout="wide")

st.title("⚡ Find Nearby EV Charging Stations")
st.write("Enter a city or location to find nearby EV charging points with distance and route link.")

# --- User Input ---
location_input = st.text_input("🔍 Enter location (e.g., Mumbai, Delhi, Bangalore):")

# --- Your OpenChargeMap API key ---
API_KEY = "594bbba0-5e98-4f63-8745-bfccae25729f"

if location_input:
    try:
        geolocator = Nominatim(user_agent="ev_locator")
        location = geolocator.geocode(location_input, timeout=10)
    except Exception as e:
        st.error("⚠️ Location service error. Please try again later.")
        location = None

    if location:
        lat, lon = location.latitude, location.longitude
        st.success(f"📍 Found location: {location.address}")

        # --- Fetch nearby charging stations ---
        url = f"https://api.openchargemap.io/v3/poi/?output=json&latitude={lat}&longitude={lon}&distance=10&distanceunit=KM&key={API_KEY}"

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            stations = response.json() if response.text else []
        except Exception as e:
            st.warning("⚠️ Could not fetch live data. Showing demo stations instead.")
            stations = []

        # --- Fallback demo data ---
        if not stations:
            stations = [
                {
                    "AddressInfo": {
                        "Latitude": lat + 0.01,
                        "Longitude": lon + 0.01,
                        "Title": "Demo Station 1",
                        "AddressLine1": location_input,
                    }
                },
                {
                    "AddressInfo": {
                        "Latitude": lat - 0.01,
                        "Longitude": lon - 0.01,
                        "Title": "Demo Station 2",
                        "AddressLine1": location_input,
                    }
                },
            ]

        # --- Create map ---
        m = folium.Map(location=[lat, lon], zoom_start=12)
        folium.Marker(
            [lat, lon],
            popup="📍 Your Location",
            icon=folium.Icon(color="blue", icon="user", prefix="fa"),
        ).add_to(m)

        # --- Display charging station info ---
        st.markdown("### 🔋 Nearby Charging Stations:")
        for station in stations[:20]:
            info = station["AddressInfo"]
            station_lat = info["Latitude"]
            station_lon = info["Longitude"]

            # Calculate distance
            distance_km = round(geodesic((lat, lon), (station_lat, station_lon)).km, 2)

            # Google Maps route link
            maps_url = f"https://www.google.com/maps/dir/{lat},{lon}/{station_lat},{station_lon}"

            # Display info
            st.markdown(f"""
            **🔌 {info.get('Title', 'Unknown Station')}**  
            - 📍 Address: {info.get('AddressLine1', 'N/A')}  
            - 📏 Distance: **{distance_km} km**  
            - 🗺️ [Get Directions]({maps_url})  
            """)

            # Add station marker
            folium.Marker(
                [station_lat, station_lon],
                popup=f"<b>{info['Title']}</b><br>{info['AddressLine1']}<br>{distance_km} km away<br><a href='{maps_url}' target='_blank'>Open in Google Maps</a>",
                icon=folium.Icon(color="green", icon="bolt", prefix="fa"),
            ).add_to(m)

        st_folium(m, width=850, height=550)

    else:
        st.error("❌ Location not found. Please enter a valid city or area.")
else:
    st.info("👆 Enter a location above to search for EV charging stations.")
