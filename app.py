import streamlit as st
import pandas as pd
import folium
from geopy.geocoders import Nominatim

# Load the festival data
@st.cache
def load_data():
    return pd.read_csv('festivals_data.csv')

festivals_tot = load_data()

# Extract 'Year' and 'Month' from the 'Date' column
festivals_tot['Date'] = pd.to_datetime(festivals_tot['Date'])
festivals_tot['Year'] = festivals_tot['Date'].dt.year
festivals_tot['Month'] = festivals_tot['Date'].dt.month

# Sidebar options
year_options = sorted(festivals_tot['Year'].unique())
selected_year = st.sidebar.selectbox('Select Year', year_options)

month_options = sorted(festivals_tot['Month'].unique())
selected_month = st.sidebar.selectbox('Select Month', month_options)

country_options = sorted(festivals_tot['Country'].unique())
selected_country = st.sidebar.selectbox('Select Country', country_options)

category_options = sorted(festivals_tot['Category'].unique())
selected_category = st.sidebar.selectbox('Select Category', category_options)

price_range_options = ['< 50', '50 - 100', '100 - 150', '150 - 200', '> 200']
selected_price_range = st.sidebar.selectbox('Select Price Range', price_range_options)

# Filter the DataFrame based on selected options
filtered_df = festivals_tot[
    (festivals_tot['Year'] == selected_year) &
    (festivals_tot['Month'] == selected_month) &
    (festivals_tot['Country'] == selected_country) &
    (festivals_tot['Category'] == selected_category) &
    (festivals_tot['Price'] <= int(selected_price_range.split(' ')[0])) &
    (festivals_tot['Price'] >= int(selected_price_range.split(' ')[-1]))
]

# Display the filtered subset DataFrame
st.write(filtered_df)

# Create a map of Europe
m = folium.Map(location=[51.1657, 10.4515], zoom_start=5)

# Initialize geocoder
geolocator = Nominatim(user_agent="festivals_app")

# Add markers for festivals
for _, row in filtered_df.iterrows():
    # Geocode location
    location = geolocator.geocode(row['Venue'])
    if location:
        latitude = location.latitude
        longitude = location.longitude
        folium.Marker(location=[latitude, longitude], popup=row['Name']).add_to(m)

# Display the map
st.write(m)

# Example: Run the Streamlit script directly
if __name__ == '__main__':
    st.set_page_config(layout="wide")  # Set the page layout to wide
    from app import main  # Import your Streamlit script
    main()  # Run the Streamlit application
