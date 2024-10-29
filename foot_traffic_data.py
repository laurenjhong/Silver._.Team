import pandas as pd
import numpy as np
import random
import openai

# Set up OpenAI API key
openai.api_key = "your_openai_api_key"

# Generate random restaurant names and zip codes
restaurant_names = ["Burger Haven", "Pizza Palace", "Taco Town", "Sushi Spot", "Grill House", 
                    "Pasta Place", "Bistro Bites", "Steak Station", "Salad Central", "Wrap World"]
zip_codes = ["10001", "90001", "60601", "30301", "80201", "94101", "33101", "75201", "98101", "85001"]

# Generate sample data for a month (30 days)
dates = pd.date_range(start="2023-10-01", end="2023-10-30")
days = dates.strftime("%A")  # Days of the week
foot_traffic_volume = [random.randint(50, 500) for _ in range(len(dates))]  # Random foot traffic numbers
inventory_used = [round(traffic * random.uniform(0.3, 0.6)) for traffic in foot_traffic_volume]  # Approximate inventory
staffing_hours = [round(traffic * random.uniform(0.05, 0.15), 2) for traffic in foot_traffic_volume]  # Approximate staffing hours
restaurant_name = [random.choice(restaurant_names) for _ in range(len(dates))]  # Random restaurant names
zip_code = [random.choice(zip_codes) for _ in range(len(dates))]  # Random zip codes

# Create DataFrame
data = pd.DataFrame({
    "Date": dates,
    "Day": days,
    "Restaurant Name": restaurant_name,
    "Zip Code": zip_code,
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
def predict_needs(restaurant, foot_traffic):
    # Generate OpenAI prompt
    prompt = (f"For a restaurant named '{restaurant}' with an expected foot traffic volume of {foot_traffic}, "
              "estimate the necessary inventory and staffing hours required.")
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=50
    )
    return response.choices[0].text.strip()

# Example of using OpenAI with generated data
for i in range(5):  # Example with first 5 entries
    restaurant = data["Restaurant Name"].iloc[i]
    foot_traffic = data["Foot Traffic Volume"].iloc[i]
    prediction = predict_needs(restaurant, foot_traffic)
    print(f"Predictions for {restaurant} with Foot Traffic Volume of {foot_traffic}:")
    print(prediction)
    print("-" * 30)
