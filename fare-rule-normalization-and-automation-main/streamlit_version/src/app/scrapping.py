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


# Get url with the airline company IATA Code
def get_url_from_db(iata_code):
    filtered_df = DF[DF["IATA"] == iata_code]

    if not filtered_df.empty:
        # Access the url value from the filtered DataFrame
        url_for_iata = filtered_df["website"].iloc[0]
        return url_for_iata
    else:
        print(f"No match found for IATA code {iata_code}")
        return False


# Scrap text with IATA Code
def scrap_text_from_iata(iata_code):
    url = get_url_from_db(iata_code)

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
        print("Url doesn't exist")
        return None


# print(scrap_text_from_iata("QR"))
# print(scrap_text_from_iata("AC"))
# print(scrap_text_from_iata("B6"))
# print(scrap_text_from_iata("RJ"))
