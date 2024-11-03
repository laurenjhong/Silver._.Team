import streamlit as st
import openai
import os
import pandas as pd
import collections

# Set your OpenAI API key here
openai.api_key = os.getenv('OPENAI_API_KEY')

# Function to generate insights using OpenAI
def generate_insights(zip_code, business_type, foot_traffic_volume):
    prompt = f"Provide detailed insights for the area with zip code {zip_code}, focusing on the business type '{business_type}' with a foot traffic volume of {foot_traffic_volume}."
    response = openai.Completion.create(
        model="gpt-3.5-turbo-instruct",
        prompt=prompt,
        max_tokens=150
    )
    return response.choices[0].text.strip()

# Read data from pre-existing CSV file
csv_file = 'full_year_business_data.csv'  # Ensure this file exists in your directory
df = pd.read_csv(csv_file)

# Convert 'Foot Traffic Volume' to numeric, forcing any errors to be NaN, then filling NaNs with 0
df['Foot Traffic Volume'] = pd.to_numeric(df['Foot Traffic Volume'], errors='coerce').fillna(0)

# Streamlit app
st.title('Business Foot Traffic Analysis')

# Create columns for dropdown menus
col1, col2 = st.columns(2)

# Create dropdown menus for users to select business type and area code in the respective columns
with col1:
    selected_business_type = st.selectbox('Select Business Type', df['Business Type'].unique())
with col2:
    selected_zip_code = st.selectbox('Select Zip Code', df['Zip Code'].unique())

# Filter the data based on the selected business type and area code
filtered_df = df[(df['Business Type'] == selected_business_type) & (df['Zip Code'] == selected_zip_code)]

# Display the filtered data
st.write(f'### Data for {selected_business_type} in zip code {selected_zip_code}')
st.dataframe(filtered_df)

# Analyze the data to find the business type with the highest foot traffic based on area code
business_count_by_zip = collections.Counter()
for row in filtered_df.itertuples(index=False):
    _, business_name, business_type, zip_code, latitude, longitude, foot_traffic_volume, _, _, _, _ = row
    business_count_by_zip[(business_type, zip_code)] += foot_traffic_volume

# Find the business type with the highest count in each zip code
highest_traffic_by_zip = {}
for key, count in business_count_by_zip.items():
    business_type, zip_code = key
    if zip_code not in highest_traffic_by_zip or count > highest_traffic_by_zip[zip_code][1]:
        highest_traffic_by_zip[zip_code] = (business_type, count)

# Display the highest traffic business type by zip code
st.write('### Highest Traffic Business Type by Zip Code')
for zip_code, (business_type, count) in highest_traffic_by_zip.items():
    st.write(f"Highest traffic in area code {zip_code}: {business_type} with {count} visitors")

# Generate and display additional insights using OpenAI
if st.button("Generate Insights"):
    if not filtered_df.empty:
        foot_traffic_volume = filtered_df['Foot Traffic Volume'].sum()
        insights = generate_insights(selected_zip_code, selected_business_type, foot_traffic_volume)
        st.write('### Additional Insights')
        st.write(insights)
    else:
        st.write("No data available for the selected filters.")
