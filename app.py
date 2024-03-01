import streamlit as st
import pandas as pd
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium

# Define the HTML code
html_code = """
<!-- &lt;meta http-equiv=&quot;content-type&quot; content=&quot;text/html; charset=UTF-8&quot; /&gt;

    &lt;script&gt;
        L_NO_TOUCH = false;
        L_DISABLE_3D = false;
    &lt;/script&gt;

&lt;style&gt;html, body {width: 100%;height: 100%;margin: 0;padding: 0;}&lt;/style&gt;
&lt;style&gt;#map {position:absolute;top:0;bottom:0;right:0;left:0;}&lt;/style&gt;
&lt;script src=&quot;https://cdn.jsdelivr.net/npm/leaflet@1.9.3/dist/leaflet.js&quot;&gt;&lt;/script&gt;
&lt;script src=&quot;https://code.jquery.com/jquery-3.7.1.min.js&quot;&gt;&lt;/script&gt;
&lt;script src=&quot;https://cdn.jsdelivr.net/npm/bootstrap@5.2.2/dist/js/bootstrap.bundle.min.js&quot;&gt;&lt;/script&gt;
&lt;script src=&quot;https://cdnjs.cloudflare.com/ajax/libs/Leaflet.awesome-markers/2.0.2/leaflet.awesome-markers.js&quot;&gt;&lt;/script&gt;
&lt;link rel=&quot;stylesheet&quot; href=&quot;https://cdn.jsdelivr.net/npm/leaflet@1.9.3/dist/leaflet.css&quot;/&gt;
&lt;link rel=&quot;stylesheet&quot; href=&quot;https://cdn.jsdelivr.net/npm/bootstrap@5.2.2/dist/css/bootstrap.min.css&quot;/&gt;
&lt;link rel=&quot;stylesheet&quot; href=&quot;https://netdna.bootstrapcdn.com/bootstrap/3.0.0/css/bootstrap.min.css&quot;/&gt;
&lt;link rel=&quot;stylesheet&quot; href=&quot;https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@6.2.0/css/all.min.css&quot;/&gt;
&lt;link rel=&quot;stylesheet&quot; href=&quot;https://cdnjs.cloudflare.com/ajax/libs/Leaflet.awesome-markers/2.0.2/leaflet.awesome-markers.css&quot;/&gt;
&lt;link rel=&quot;stylesheet&quot; href=&quot;https://cdn.jsdelivr.net/gh/python-visualization/folium/folium/templates/leaflet.awesome.rotate.min.css&quot;/&gt;

        &lt;meta name=&quot;viewport&quot; content=&quot;width=device-width,
            initial-scale=1.0, maximum-scale=1.0, user-scalable=no&quot; /&gt;
        &lt;style&gt;
            #map_f228749a05882d9f7c784bd8ccc1139f {
                position: relative;
                width: 100.0%;
                height: 100.0%;
                left: 0.0%;
                top: 0.0%;
            }
            .leaflet-container { font-size: 1rem; }
        &lt;/style&gt;-->
<meta http-equiv="content-type" content="text/html; charset=UTF-8" />
<script>
    L_NO_TOUCH = false;
    L_DISABLE_3D = false;
</script>
<style>html, body {width: 100%;height: 100%;margin: 0;padding: 0;}</style>
<style>#map {position:absolute;top:0;bottom:0;right:0;left:0;}</style>
<script src="https://cdn.jsdelivr.net/npm/leaflet@1.9.3/dist/leaflet.js"></script>
<script src="https://code.jquery.com/jquery-3.7.1.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.2/dist/js/bootstrap.bundle.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/Leaflet.awesome-markers/2.0.2/leaflet.awesome-markers.js"></script>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/leaflet@1.9.3/dist/leaflet.css"/>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.2/dist/css/bootstrap.min.css"/>
<link rel="stylesheet" href="https://netdna.bootstrapcdn.com/bootstrap/3.0.0/css/bootstrap.min.css"/>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@6.2.0/css/all.min.css"/>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/Leaflet.awesome-markers/2.0.2/leaflet.awesome-markers.css"/>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/python-visualization/folium/folium/templates/leaflet.awesome.rotate.min.css"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />
<style>
    #map_f228749a05882d9f7c784bd8ccc1139f {
        position: relative;
        width: 100.0%;
        height: 100.0%;
        left: 0.0%;
        top: 0.0%;
    }
    .leaflet-container { font-size: 1rem; }
</style>
"""

# Render the HTML code in Streamlit
st.markdown(html_code, unsafe_allow_html=True)


# Load the festival data
@st.cache_data # This decorator ensures that the data is loaded only once
def load_data():
    return pd.read_csv('festivals_tot.csv')

festivals_tot = load_data()

# Extract 'Year' and 'Month' from the 'Date' column
festivals_tot['Date'] = pd.to_datetime(festivals_tot['Date'])
festivals_tot['Year'] = festivals_tot['Date'].dt.year
festivals_tot['Month'] = festivals_tot['Date'].dt.month

year_options = sorted(festivals_tot['Year'].unique())
year_options = ['Any'] + year_options  # Add 'Any' option
selected_year = st.sidebar.selectbox('Select Year', year_options)

month_options = sorted(festivals_tot['Month'].unique())
month_options = ['Any'] + month_options  # Add 'Any' option
selected_month = st.sidebar.selectbox('Select Month', month_options)

country_options = sorted(festivals_tot['Country'].unique())
country_options = ['Any'] + country_options  # Add 'Any' option
selected_country = st.sidebar.selectbox('Select Country', country_options)

category_options = sorted(festivals_tot['Category'].unique())
category_options = ['Any'] + category_options  # Add 'Any' option
selected_category = st.sidebar.selectbox('Select Category', category_options)

price_range_options = ['< 50', '50 - 100', '100 - 150', '150 - 200', '> 200']
price_range_options = ['Any'] + price_range_options  # Add 'Any' option
selected_price_range = st.sidebar.selectbox('Select Price Range', price_range_options)

# Define price range boundaries
price_ranges = {
    '< 50': (0, 50),
    '50 - 100': (50, 100),
    '100 - 150': (100, 150),
    '150 - 200': (150, 200),
    '> 200': (200, float('inf'))
}

# Filter the DataFrame based on selected options
if selected_year != 'Any':
    festivals_tot = festivals_tot[festivals_tot['Year'] == selected_year]
if selected_month != 'Any':
    festivals_tot = festivals_tot[festivals_tot['Month'] == selected_month]
if selected_country != 'Any':
    festivals_tot = festivals_tot[festivals_tot['Country'] == selected_country]
if selected_category != 'Any':
    festivals_tot = festivals_tot[festivals_tot['Category'] == selected_category]
if selected_price_range != 'Any':
    festivals_tot = festivals_tot['Price(s.f.)'].between(*price_ranges[selected_price_range])

# Manually specify the width of the sidebar in pixels
sidebar_width_px = 300  # Adjust this value according to your sidebar width

# Calculate the maximum width for the table
max_table_width = "calc(100% - {}px)".format(sidebar_width_px)

# Render the DataFrame to HTML with adjusted width and precision
html_table = festivals_tot.style.set_table_styles([{
    'selector': 'table',
    'props': [('max-width', max_table_width)]
}]).set_properties(**{'font-size': '12pt'}).to_html(escape=False)

# Display the HTML table
st.write(html_table, unsafe_allow_html=True)

# Count the number of festivals per country
festivals_per_country = festivals_tot['Country'].value_counts()

# Create a base map of Europe
m = folium.Map(location=[51.1657, 10.4515], zoom_start=5)

# Add a heatmap layer with festival counts per country
heat_data = []
for country, count in festivals_per_country.items():
    # Check if Latitude and Longitude columns exist
    if "Latitude" in festivals_tot.columns and "Longitude" in festivals_tot.columns:
        # Check if the country entry is a list of coordinates
        if isinstance(country, list):
            # Iterate over the coordinates and add non-NaN values to the heatmap data
            for coord in country:
                if not any(map(lambda x: pd.isnull(x), coord)):  # Check for NaN values
                    heat_data.append([coord[0], coord[1], count])  # Append latitude, longitude, count
        else:
            # Retrieve latitude and longitude corresponding to the country
            lat = festivals_tot.loc[festivals_tot['Country'] == country, 'Latitude'].iloc[0]
            lon = festivals_tot.loc[festivals_tot['Country'] == country, 'Longitude'].iloc[0]
            # Check if latitude and longitude are not NaN before adding to heatmap data
            if not (pd.isnull(lat) or pd.isnull(lon)):
                heat_data.append([lat, lon, count])  # Append latitude, longitude, count
    else:
        # Add country name as the tooltip for the heatmap
        heat_data.append([country, count])

# Add heatmap layer to the map
HeatMap(heat_data, min_opacity=0.5, max_zoom=18, radius=15, blur=10).add_to(m)

# Display the map
st_folium(m, width=1500, height=500)