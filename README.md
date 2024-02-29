# European music festival dataset

![Festival](festival.jpg)

This project consists of several parts:
1. **Scraping data** from https://www.festival-alarm.com/us using BeautifulSoup. After some research, this website seemed to be the only one providing a decent overview of European music festivals from 2014 to 2025. The tables from the different pages corresponding to each year were merged to form a single Pandas Dataframe. From a first analysis it´s clear that the dataset has not been curated and presents many missing values especially when counting the number of visitors and the price of tickets(ca. 30% each). Furthermore many well known festivals have not been reported and the dataframe shows to be accurate only for countries like Germany and UK, while for other countries like Italy it shows too few entries (only 17 in total, which is obviously not accurate). This Dataset could be improved integrating information from different sources, like Wikipedia for instance.
2. **Data cleaning** After parsing the HTML file in step 1, the resulting Dataframe had 11 column, which required several cleaning steps. These included: data type conversion, string cleaning (like separating or merging words), datetime feature extraction etc.
3. **Feature Engineering** Dates were rendered in a uniform way to present just the day of start of the event. Since we have a column for 'Duration', this information seemed redundant, and not easy to handle for data analysis if we don´t have uniform format of data in a particular column. An additional column 'Total_revenue' was created by simply multipling the number of visitors for the price. Further analysis could be interesting, to have a better estimation of this value. Also with all the missing values, and not having implemented any soluition to fill them, we could calculate the revenue for only ca. 50% of the rows.
4. **Geocoding Location** using Nominatim. Thisn allows to create two new columns 'Latitude' and 'Longitude' with coordinates that can be used to display the entries on a map
5. **Data Analysis** some consideration and visualization on the data
6. **Streamlit App**: an interactive visualization of the mapping applying different filters

## Requirements
Python version: `3.11.8`
```
pip install -r requirements.txt
```

## Streamlit app
The streamlit app allows to visualize subsets of the dataset. Select the properties for a specific subset and display it on the map.  

Run the streamlit app from the console with:

```
streamlit run app.py
``` 