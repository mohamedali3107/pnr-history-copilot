import pandas as pd
import requests
from bs4 import BeautifulSoup

# Constants
DB_PATH = "website_list.xlsx"
DF = pd.read_excel(DB_PATH)

headers = {
    "authority": "www.google.com",
    "accept": "text/html,application/json, text/plain, application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "en-US,en;q=0.9",
    "cache-control": "max-age=0",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "connection": "keep-alive",
    "accept-encoding": "gzip, deflate, br",
}


def get_url_from_db(airline_iata_code):
    """
    Fetch the url of the webpage corresponding to the Airline IATA Code from the website_list.xlsx database.

    Parameters:
    - airline_iata_code (str): The Airline IATA Code.

    Returns:
    - url_for_iata (str): The corresponding webpage url if it exists.
    - False (boolean): otherwise
    """
    filtered_df = DF[DF["IATA"] == airline_iata_code]

    if not filtered_df.empty:
        # Access the url value from the filtered DataFrame
        url_for_iata = filtered_df["website"].iloc[0]
        return url_for_iata
    else:
        return False


def scrape_text_from_iata(airline_iata_code):
    """
    Scrape the text from the webpage retrieve thanks to the Airline IATA Code.

    Parameters:
    - airline_iata_code (str): The Airline IATA Code.

    Returns:
    - text_content (str): The text scraped from the webpage if the url exists and the scraping works.
    - None: otherwise
    """
    url = get_url_from_db(airline_iata_code)

    if url:
        response = requests.get(url, headers=headers)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the HTML content with BeautifulSoup
            soup = BeautifulSoup(response.content, "html.parser")

            # Find and print the text content
            text_content = soup.get_text()
            text_content = text_content.replace("\n", " ")
            return text_content
        else:
            print(f"Failed to retrieve content. Status code: {response.status_code}")
            return None
    else:
        return None
