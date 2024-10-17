# Import necessary libraries for web scraping and data manipulation
from bs4 import BeautifulSoup
import requests
import pandas as pd

# Create a DataFrame to store the safety data for different vehicle types
df = pd.DataFrame(columns=['type', 'rank', 'year', 'make', 'model', 'rsc_rating', 'fatality_risk', 'injury_risk'])

# List of vehicle body types to iterate over
body_types = ['sedans', 'suvs', 'pickups', 'vans']

# Base URL for the website to be scraped
base_url = "https://realsafecars.com/"

def get_soup(body_type, page):
    """
    Fetches and parses the HTML content of a webpage.

    Parameters:
    - body_type (str): Type of vehicle body (e.g., 'sedans', 'suvs')
    - page (int): Page number to fetch data from

    Returns:
    - BeautifulSoup object containing parsed HTML content
    """
    # Construct the URL based on the body type and page number
    if page == 1:
        url_page = "/all"  # First page
    else:
        url_page = "/" + str(page)  # Subsequent pages

    url = base_url + f"{body_type}" + url_page

    # Send a GET request to the URL and get the HTML content
    response = requests.get(url)
    html_content = response.content

    # Parse the HTML content using BeautifulSoup and return the soup object
    return BeautifulSoup(html_content, "html.parser")

def get_max_pages(body_type):
    """
    Finds the maximum number of pages available for a given body type.

    Parameters:
    - body_type (str): Type of vehicle body

    Returns:
    - int: Maximum page number found
    """
    # Get the soup for the first page to find pagination information
    soup = get_soup(body_type=body_type, page=1)
    
    # Find all page number links to determine the total number of pages
    pagination_links = soup.find_all("a", class_="MuiPaginationItem-page")
    page_nums = []

    # Extract page numbers from the pagination links
    for i in range(len(pagination_links)):
        page_value = pagination_links[i].text
        if page_value == '':  # Skip empty values
            continue
        page_nums.append(int(page_value))

    # Return the highest page number found
    return max(page_nums)

def add_data_from_page(body_type, page):
    """
    Scrapes data from a specific page and appends it to the global DataFrame.

    Parameters:
    - body_type (str): Type of vehicle body
    - page (int): Page number to scrape data from
    """
    global df
    # Get the soup for the current page
    soup = get_soup(body_type=body_type, page=page)

    # Loop through each row of the table containing vehicle data
    for row in soup.find_all("tr", class_="Tables__TR-f84ad0-2 dxGljX"):
        # Find all table cells in the row
        cells = row.find_all("td", class_="Tables__TD-f84ad0-3")

        # Check if the row has at least the expected number of cells
        if len(cells) >= 5:
            rank = cells[0].get_text(strip=True)
            
            # Split the vehicle name to extract year, make, and model
            name = cells[1].get_text(strip=True).split()
            year = name[0]
            make = name[1]
            model = " ".join(name[2:])
            
            # Extract ratings and risk data from the remaining cells
            rsc_rating = cells[2].get_text(strip=True)
            fatality_risk = cells[3].get_text(strip=True)
            injury_risk = cells[4].get_text(strip=True)

            # Create a new DataFrame row with the extracted data
            new_row = pd.DataFrame({
                'type': [body_type],
                'rank': [rank],
                'year': [year],
                'make': [make],
                'model': model,
                'rsc_rating': [rsc_rating],
                'fatality_risk': [fatality_risk],
                'injury_risk': [injury_risk]
            })

            # Append the new row to the global DataFrame
            df = pd.concat([df, new_row], ignore_index=True)

def main():
    """
    Main function to iterate through vehicle types and their pages,
    scraping data and saving it to a CSV file.
    """
    global df
    # Iterate over each vehicle body type
    for type in body_types:
        # Get the maximum number of pages for the current body type
        max_pages = get_max_pages(body_type=type)
        
        # Iterate over each page to scrape data
        for page in range(1, max_pages + 1):
            add_data_from_page(body_type=type, page=page)
    
    # Save the collected data to a CSV file
    df.to_csv("safety-data.csv")

# Run the main function
main()