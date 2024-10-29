import pandas as pd
import numpy as np
import random
import openai

# Set up OpenAI API key
openai.api_key = "api-key"

# Generate sample data for a month (30 days)
dates = pd.date_range(start="2023-10-01", end="2023-10-30")
days = dates.strftime("%A")  # Days of the week
foot_traffic_volume = [random.randint(50, 500) for _ in range(len(dates))]  # Random foot traffic numbers
inventory_used = [round(traffic * random.uniform(0.3, 0.6)) for traffic in foot_traffic_volume]  # Approximate inventory
staffing_hours = [round(traffic * random.uniform(0.05, 0.15), 2) for traffic in foot_traffic_volume]  # Approximate staffing hours

# Create DataFrame
data = pd.DataFrame({
    "Date": dates,
    "Day": days,
    "Foot Traffic Volume": foot_traffic_volume,
    "Inventory Used": inventory_used,
    "Staffing Hours": staffing_hours
})

# Save to CSV (optional)
data.to_csv("sample_foot_traffic_data.csv", index=False)

# Display sample data
print("Sample Data:")
print(data.head())

# Function to use OpenAI for predicting inventory and staffing needs
def predict_needs(foot_traffic):
    # Generate OpenAI prompt
    prompt = f"Given a foot traffic volume of {foot_traffic}, estimate the necessary inventory and staffing hours required for a retail store."
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=50
    )
    return response.choices[0].text.strip()

# Example of using OpenAI with generated data
for i in range(5):  # Example with first 5 entries
    foot_traffic = data["Foot Traffic Volume"].iloc[i]
    prediction = predict_needs(foot_traffic)
    print(f"Predictions for Foot Traffic Volume of {foot_traffic}:")
    print(prediction)
    print("-" * 30)