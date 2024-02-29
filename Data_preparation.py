import requests
import pandas as pd
from bs4 import BeautifulSoup
import re

def DataScraper(url):
    """
    This function takes in the url and finds the table

    Returns:
    table content as HTML code
    """
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    table = soup.find('table',
                      {'class':'data-table table table-primary table-striped festival_table tableWithFilter'})
    return table

def TableToDataFrame(table):
    """
    This function takes in the table and converts it into a dataframe
    after applying minimal data cleaning

    Returns:
    table as a dataframe
    """
    # Extract column names from <th> elements
    columns = [th.text for th in table.find_all('th')]
    tableValues = [] # Create an empty list to store the table values
    for x in table.find_all('tr')[1:]: # Skipping the first row which is the table header
        td_tags = x.find_all('td')
        td_val = [y.text for y in td_tags]
        tableValues.append(td_val)

    # Clean each string in the table data removing newlines (\n) and whitespaces
    cleaned_data = [[cell.strip().replace('\n', '').strip() for cell in row] for row in tableValues]
    cleaned_data = [[cell.strip().replace(' ', '').strip() for cell in row] for row in tableValues]

    # Number of rows of cleaned_data
    num_rows = len(cleaned_data)

    # Number of columns (assuming all rows have the same number of elements)
    num_columns = len(cleaned_data[0])
    # Create a list of empty dictionaries
    empty_data = [{} for _ in range(num_rows)]

    # Create DataFrame
    df = pd.DataFrame(empty_data, columns=columns)

    # Assign elements of cleaned_data to the DataFrame
    for x in range (len(cleaned_data[:])):
        for y in range(num_columns):
            df.iat[x,y] = cleaned_data[x][y]
    
    # Select the first 10 columns (the last one was the link to the website, so we´re going to drop it) and all rows
    selected_columns = df.iloc[:, :10]

    # Create a new DataFrame with the selected columns and all rows
    final_df = pd.DataFrame(selected_columns)

    return final_df

def improve_readability(col):
    """
    This function improves the readability of the column names
    by putting spaces between different words, recognized by capital letters

    It takes a list or a column as input and returns its improved version
    """
    # Insert whitespace before each capital letter (excluding the first)
    improved_name = re.sub(r'(?<!^)(?=[A-Z])', ' ', col)
    return improved_name

def rewrite_date(date, year):
    """
    This function rewrites the date format in a human-readable format by adding the year
    and removing the \n-\n\n still present from the HTML file. It also ignores single-day events.
    """
    # Check if the date range format is present
    if '\n-\n\n' in date:
        # Split the date range into start and end dates
        start_date, end_date = date.split('\n-\n\n')
        # Join the start and end dates with a hyphen and add the year
        rewritten_date = f"{start_date}/{year} - {end_date}/{year}"
    else:
        # If the date range format is not present, return the original date with the year
        rewritten_date = f"{date}/{year}"
    return rewritten_date.strip()  # Strip any leading or trailing whitespace


def extract_duration(duration):
    """
    This function extracts the numeric part of the duration
    """
    # Extract numeric part using regular expression
    numeric_part = int(''.join(filter(str.isdigit, duration)))
    return numeric_part

def remove_festivals(category):
    """
    This function removes the word "festivals" from the category
    """
    # Remove "festivals" substring
    category_without_festivals = category.replace("festivals", "")
    return category_without_festivals.strip()  # Strip any leading or trailing whitespace

def clean_venue(venue):
    """
    This function substitutes the string "\n" with " "
    """

    venue_cleaned = venue.replace("\n", " ")
    return venue_cleaned

def clean_price(price):
    """
    This function removes the currency symbol and converts the price to a float
    """
    # Handling the cases where the price is 'n/a'
    if price == 'n/a':
        return pd.NA
    
    price_cleaned = float(price.replace("€", "").replace(",", ""))
    return price_cleaned

def beginning_converter(date_str):
    """
    This function converts dates presented as a range into the date 
    of event beginning
    """
     # Define a regular expression pattern to match date range format
    pattern = r'\d{2}/\d{2}/\d{4} - \d{2}/\d{2}/\d{4}'
    
    # Check if the input string matches the date range pattern
    if re.match(pattern, date_str):
        # Split the date range string and return the first date
        return date_str.split(' - ')[0]
    else:
        # Return the input string unchanged
        return date_str


def convert_to_datetime(column):
    """
    Convert elements in a column to datetime format.
    If the element is already in datetime format, it is left unchanged.
    """
    # Convert to strings
    # column = column.convert_dtypes(convert_string=True)

    # Convert individual dates to datetime
    column = pd.to_datetime(column, errors='coerce')

    return column

def merge_capital_words(string):
    """
    Merge single capital letters in a string
    It can be used to form country-code for instance
    """
    words = string.split()
    merged_words = [words[0]]
    
    for i in range(1, len(words)):
        current_word = words[i]
        previous_word = words[i - 1]
        
        # Check if both current and previous words have length 1 and are capital letters
        if len(current_word) == 1 and len(previous_word) == 1 and current_word.isupper() and previous_word.isupper():
            merged_words[-1] += current_word  # Merge current word with previous word
        else:
            merged_words.append(current_word)  # Add current word as is
    
    return ' '.join(merged_words)

def split_and_newline(genres_string):
    # Split the string by ","
    genres_list = genres_string.split(',')
    # Join the elements of the list with newline characters
    return '\n'.join(genres_list)