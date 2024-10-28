import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from folium.plugins import HeatMap

# Set page config
st.set_page_config(page_title="Foot Traffic Heat Map", layout="wide")

# Load Data
@st.cache_data
def load_data(file_path):
    data = pd.read_csv(file_path)
    return data

# Input for the data file (upload CSV or choose a sample file path)
uploaded_file = st.file_uploader("Choose a CSV file with latitude, longitude, and weight columns", type="csv")
if uploaded_file:
    data = pd.read_csv(uploaded_file)
else:
    # Sample synthetic data if no file is uploaded
    data = pd.DataFrame({
        'latitude': [37.7749, 37.7749, 37.7750, 37.7750],
        'longitude': [-122.4194, -122.4192, -122.4193, -122.4190],
        'weight': [1, 2, 3, 4]
    })

# Display data
st.write("Data Preview", data.head())

# Define the map centered around the average location
m = folium.Map(location=[data['latitude'].mean(), data['longitude'].mean()], zoom_start=14)

# Add HeatMap layer
heat_data = [[row['latitude'], row['longitude'], row['weight']] for index, row in data.iterrows()]
HeatMap(heat_data).add_to(m)

# Display map with Streamlit
st_folium(m, width=700, height=500)

#This has all been ChatGPT assisted
