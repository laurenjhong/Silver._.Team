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

# Display app title
st.title("Foot Traffic Heat Map")

# Display app description
st.write("This Streamlit app visualizes foot traffic volume using a heat map. Upload a CSV file containing latitude, longitude, and foot traffic volume data to see the areas with the highest and lowest foot traffic.")

# Input for the data file (upload CSV or choose a sample file path)
uploaded_file = st.file_uploader("Choose a CSV file with latitude, longitude, and weight columns", type="csv")
if uploaded_file:
    data = pd.read_csv(uploaded_file)

    # Filter necessary columns
    data = data[['Latitude', 'Longitude', 'Foot Traffic Volume', 'Zip Code', 'Business Type']]

    # Find most and least popular zip codes for restaurants
    restaurants = data[data['Business Type'] == 'Restaurant']
    most_popular_restaurants = restaurants.groupby('Zip Code')['Foot Traffic Volume'].sum().nlargest(5).reset_index()
    least_popular_restaurants = restaurants.groupby('Zip Code')['Foot Traffic Volume'].sum().nsmallest(5).reset_index()

    # Find most and least popular zip codes for stores
    stores = data[data['Business Type'] == 'Store']
    most_popular_stores = stores.groupby('Zip Code')['Foot Traffic Volume'].sum().nlargest(5).reset_index()
    least_popular_stores = stores.groupby('Zip Code')['Foot Traffic Volume'].sum().nsmallest(5).reset_index()

    # Display the results
    st.write("### Top 5 Most Popular Zip Codes for Restaurants")
    st.table(most_popular_restaurants)

    st.write("### Top 5 Least Popular Zip Codes for Restaurants")
    st.table(least_popular_restaurants)

    st.write("### Top 5 Most Popular Zip Codes for Stores")
    st.table(most_popular_stores)

    st.write("### Top 5 Least Popular Zip Codes for Stores")
    st.table(least_popular_stores)

    # Define the map centered around the average location
    m = folium.Map(location=[data['Latitude'].mean(), data['Longitude'].mean()], zoom_start=14)

    # Add HeatMap layer
    heat_data = [[row['Latitude'], row['Longitude'], row['Foot Traffic Volume']] for index, row in data.iterrows()]
    HeatMap(heat_data).add_to(m)

    # Display map with Streamlit and add a title
    st.write("### Foot Traffic Heat Map")
    st_folium(m, width=900, height=600)
else:
    st.write("Please upload a CSV file to display the heat map.")