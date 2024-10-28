import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Sample data (hourly foot traffic for a day)
foot_traffic_data = {
    "Hour": list(range(24)),
    "Foot Traffic": [30, 45, 60, 85, 100, 150, 200, 300, 500, 400, 300, 200,
                     150, 100, 80, 60, 45, 30, 25, 20, 15, 10, 5, 3]
}

df = pd.DataFrame(foot_traffic_data)

# Set Hour as index for the heatmap
df.set_index("Hour", inplace=True)

# Plot the heatmap using Seaborn
st.title("Foot Traffic Heatmap & Staffing/Inventory Needs")
st.write("This heatmap shows foot traffic patterns throughout the day.")

plt.figure(figsize=(10, 1))
sns.heatmap(df.T, annot=True, cmap="YlGnBu", cbar=True)
st.pyplot(plt)

# Set parameters for staffing and inventory
customers_per_worker = st.slider("Customers per worker", min_value=5, max_value=50, value=20)
inventory_per_customer = st.slider("Inventory units per customer", min_value=1, max_value=10, value=2)

# Calculate staffing and inventory needs
df['Workers Needed'] = np.ceil(df['Foot Traffic'] / customers_per_worker)
df['Inventory Needed'] = df['Foot Traffic'] * inventory_per_customer

# Reset index to display the Hour column in tables
df.reset_index(inplace=True)

# Display the recommended staffing and inventory tables
st.write("Recommended Workers Per Hour:")
st.write(df[['Hour', 'Workers Needed']])

st.write("Recommended Inventory Per Hour:")
st.write(df[['Hour', 'Inventory Needed']])