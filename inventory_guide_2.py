import streamlit as st
import openai
import pandas as pd
import numpy as np
import seaborn as sns

# Set up OpenAI API key
openai.api_key = "api-key"

# OpenAI function to generate initial insights with GPT-3.5-turbo
def generate_foot_traffic_insight(month, location="San Jose"):
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant knowledgeable in restaurant data and foot traffic patterns."
        },
        {
            "role": "user",
            "content": (
                f"Provide estimated daily foot traffic patterns for a new restaurant in {location} "
                f"for the month of {month}. Include factors like weekends, weekday differences, "
                f"and suggest average traffic numbers."
            )
        }
    ]
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=150
    )
    return response['choices'][0]['message']['content']

# Generate simulated data based on OpenAI's suggestion
def generate_foot_traffic_data(suggestion, month):
    # Parse the suggestion to get an estimated traffic range
    avg_traffic_weekday = 200  # Assume an average (adjustable)
    avg_traffic_weekend = 300  # Assume a higher average for weekends

    # Create date range for the selected month
    dates = pd.date_range(start=f"2024-{month}-01", periods=30, freq='D')
    foot_traffic_data = []

    for date in dates:
        day = date.strftime("%A")
        traffic = np.random.normal(avg_traffic_weekday if day in ["Monday", "Tuesday", "Wednesday", "Thursday"] else avg_traffic_weekend, 50)
        inventory_needed = traffic * np.random.uniform(0.4, 0.6)
        foot_traffic_data.append([date, day, max(50, int(traffic)), int(inventory_needed)])

    return pd.DataFrame(foot_traffic_data, columns=["Date", "Day", "Foot Traffic Volume", "Inventory Needed"])

# Streamlit app
st.title("San Jose Restaurant Foot Traffic and Inventory Estimation")

# User input for month selection
month = st.selectbox("Select month for analysis:", ["10", "11", "12"])  # Use October, November, December as options

# Generate insights and data
if st.button("Generate Foot Traffic Insights"):
    suggestion = generate_foot_traffic_insight(month)
    st.write("OpenAI's Estimated Foot Traffic Insights:")
    st.write(suggestion)

    # Generate simulated data
    data = generate_foot_traffic_data(suggestion, month)
    st.write("Generated Foot Traffic Data:")
    st.dataframe(data)

    # Plot heatmap of foot traffic
    st.subheader("Heatmap of Foot Traffic Volume")
    traffic_pivot = data.pivot(index="Day", columns="Date", values="Foot Traffic Volume").fillna(0).astype(int)
    sns.heatmap(traffic_pivot, cmap="YlGnBu", annot=True, fmt="d", cbar_kws={'label': 'Foot Traffic Volume'})
    st.pyplot()

    # Plot heatmap of inventory needed
    st.subheader("Heatmap of Inventory Needed")
    inventory_pivot = data.pivot(index="Day", columns="Date", values="Inventory Needed").fillna(0).astype(int)
    sns.heatmap(inventory_pivot, cmap="OrRd", annot=True, fmt="d", cbar_kws={'label': 'Inventory Needed'})
    st.pyplot()