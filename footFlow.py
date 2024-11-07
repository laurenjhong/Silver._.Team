import streamlit as st
import pandas as pd
import openai

# Set your OpenAI API key
openai.api_key = "your_openai_api_key"

# Set page config
st.set_page_config(page_title="Foot Flow", layout="wide")

# Load Data
@st.cache_data
def load_data(file_path="san_jose_restaurant_locations_final_with_fixed_size_rate.csv"):
    data = pd.read_csv(file_path)
    return data

# Function to get detailed market information using OpenAI
def get_market_details(center_name):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Provide detailed information about {center_name} including the pros and cons, demographics, and lease/rent prices based on square footage.",
        max_tokens=150
    )
    return response.choices[0].text.strip()

# Display title and description
st.title("Foot Flow: Analyzing San Jose Foot Traffic for New Restaurants")
st.write("Explore high-foot-traffic areas in San Jose that best match your restaurant's needs. "
         "Use the options below to narrow down locations based on restaurant type and food preferences.")

# Load data directly from san_jose_restaurant_locations_final_with_fixed_size_rate.csv
data = load_data()

# Filter required columns
required_columns = ['Location Name', 'Cuisine Compatibility', 'Average Lease Rate ($/sq ft)', 'Image URL']
if not all(column in data.columns for column in required_columns):
    st.error(f"Dataset is missing one or more required columns: {', '.join(required_columns)}")
else:
    data = data[required_columns]

    # Create columns for dropdown menus
    col1, col2, col3 = st.columns(3)

    # What Kind of Restaurant Selectbox
    with col1:
        restaurant_type = st.selectbox("What kind of restaurant do you want to open?", 
                                        ["Fast Food", "Casual Dining", "Fine Dining", "Cafe", "Buffet", "Food Truck", "Other"])

    # What Kind of Food Multi-Select
    with col2:
        food_types = st.multiselect("What kind of food will you serve?", 
                                    ["Italian", "Mexican", "Chinese", "Indian", "Japanese", "American", "Mediterranean", "Vegan", "Fusion", "Other"])

    # Estimated Startup Cost Dropdown
    with col3:
        startup_costs = st.selectbox("Select your estimated startup costs:", 
                                     ["<$10,000", "$10,000-$50,000", "$50,000-$100,000", "$100,000+"])

    # Square footage input
    square_footage = st.number_input("Enter desired square footage:", min_value=100, max_value=10000, step=100)

    # Submit button
    if st.button("Submit"):
        # Filter data based on restaurant type and food types
        if restaurant_type or food_types:
            filtered_data = data[data['Cuisine Compatibility'].apply(lambda x: restaurant_type.lower() in x.lower() or any(food.lower() in x.lower() for food in food_types))]
        else:
            filtered_data = data.copy()

        # Check the initial number of rows
        st.write("Initial Data Shape:", data.shape)
        st.write("After Filter Shape:", filtered_data.shape)

        # If no matches are found after filtering
        if filtered_data.empty:
            st.write("No matching plazas found. Please adjust your selection criteria.")
        else:
            # Remove rows with any empty cells and strip any leading/trailing spaces
            filtered_data = filtered_data.dropna().applymap(lambda x: x.strip() if isinstance(x, str) else x)

            # Calculate monthly and yearly lease cost per location
            filtered_data['Monthly Lease Cost'] = filtered_data['Average Lease Rate ($/sq ft)'] * square_footage
            filtered_data['Yearly Lease Cost'] = filtered_data['Monthly Lease Cost'] * 12

            # Format the lease cost columns to show commas as thousand separators and no decimals
            filtered_data['Monthly Lease Cost'] = filtered_data['Monthly Lease Cost'].apply(lambda x: f"${x:,.0f}")
            filtered_data['Yearly Lease Cost'] = filtered_data['Yearly Lease Cost'].apply(lambda x: f"${x:,.0f}")

            # Ensure all plazas are shown by removing duplicate entries
            unique_filtered_data = filtered_data.drop_duplicates(subset=['Location Name'])

            # Reset index to avoid empty index rows in the display
            unique_filtered_data.reset_index(drop=True, inplace=True)

            # Prepare data for display in markdown table
            markdown_table = "| Image | Center Name | Monthly Lease Cost | Yearly Lease Cost |\n"
            markdown_table += "|:-----:|:-----------:|:------------------:|:-----------------:|\n"

            for index, row in unique_filtered_data.iterrows():
                markdown_table += f"| <img src='{row['Image URL']}' alt='{row['Location Name']}' width='150' height='150' /> | {row['Location Name']} | {row['Monthly Lease Cost']} | {row['Yearly Lease Cost']} |\n"

            st.markdown(markdown_table, unsafe_allow_html=True)

            # User selects multiple center names to learn more about
            selected_centers = st.multiselect("Select Centers to learn more about:", unique_filtered_data['Location Name'].unique())

            if selected_centers:
                for center_name in selected_centers:
                    details = get_market_details(center_name)
                    st.write(f"### Detailed Information about {center_name}")
                    st.write(details)
