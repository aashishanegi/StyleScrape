import requests
from bs4 import BeautifulSoup
import csv
import time

def get_salon_details(url, headers):
    try:
        # Use ScraperAPI to fetch the page
        scraperapi_url = f"http://api.scraperapi.com?api_key=2e55e28a08f26ae573d3d9e6ef2d531e&url={url}"
        response = requests.get(scraperapi_url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching salon details page: {e}")
        return None

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        details = {}
        details['name'] = soup.find('h1', class_='jsx-1805e64d3694f4e6 compney font25 fw700 color111').text.strip() if soup.find('h1', class_='jsx-1805e64d3694f4e6 compney font25 fw700 color111') else 'Name not found'
        details['address'] = soup.find('div', class_='jsx-1805e64d3694f4e6 adress font15 fw500 color111').text.strip() if soup.find('div', class_='jsx-1805e64d3694f4e6 adress font15 fw500 color111') else 'Address not found'
        details['rating'] = soup.find('div', class_='jsx-1805e64d3694f4e6 vendbox_rateavg font17 fw500 colorFFF mr-6 pointer').text.strip() if soup.find('div', class_='jsx-1805e64d3694f4e6 vendbox_rateavg font17 fw500 colorFFF mr-6 pointer') else 'Rating not found'
        details['timing'] = soup.find('span', class_='font14 fw400 color111').text.strip() if soup.find('span', class_='font14 fw400 color111') else 'Timing not found'
        details['phone'] = soup.find('a', class_='jsx-1805e64d3694f4e6 action_item_text fw600 colorFFF ml-10').text.strip() if soup.find('a', class_='jsx-1805e64d3694f4e6 action_item_text fw600 colorFFF ml-10') else 'Phone not found'
        details['yib'] = soup.find('div', class_='jsx-1805e64d3694f4e6 vendbox_ratecount font15 fw400 color111').text.strip() if soup.find('div', class_='jsx-1805e64d3694f4e6 vendbox_ratecount font15 fw400 color111') else 'Years in Business not found'
        details['Services'] = soup.find('div', class_='jsx-52f313c6d4a33388 amenities_rowbox').text.strip() if soup.find('div', class_='jsx-52f313c6d4a33388 amenities_rowbox') else 'Review not found'

        return details
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")
        return None

def scrape_justdial_salons(city):
    base_url = "https://www.justdial.com"
    url = f"{base_url}/{city}/Salons"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    # Use ScraperAPI to fetch the page
    scraperapi_url = f"http://api.scraperapi.com?api_key=2e55e28a08f26ae573d3d9e6ef2d531e&url={url}"

    try:
        response = requests.get(scraperapi_url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching page: {e}")
        return None

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract salon listings
        salons = []
        results = soup.find_all('div', class_='jsx-5a783115a9ece035 resultbox_info')

        if results:
            for result in results:
                salon = {}
                url_elem = result.find('a', class_='jsx-5a783115a9ece035 resultbox_title_anchorbox font22 fw500 color111')
                salon_url = url_elem['href'] if url_elem and 'href' in url_elem.attrs else None
                if salon_url:
                    full_url = base_url + salon_url
                    salon_details = get_salon_details(full_url, headers)
                    if salon_details:
                        salons.append(salon_details)
                    time.sleep(1)  # Sleep for 1 second to avoid making too many requests in a short time

            return salons
        else:
            print("No salon listings found.")
            return None
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")
        return None

def save_to_csv(salons, city):
    filename = f"{city}_salons.csv"
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['name', 'address', 'rating', 'timing', 'phone', 'yib', 'Services'])
        writer.writeheader()
        for salon in salons:
            writer.writerow(salon)
    print(f"Data saved to {filename}")

# List of cities to scrape salons for
cities = ['Delhi', 'Mumbai', 'Hyderabad', 'Dehradun', 'Bangalore']

# Loop through each city and scrape salons
for city in cities:
    print(f"Scraping salons for {city}...")
    salons = scrape_justdial_salons(city)

    if salons:
        save_to_csv(salons, city)
    else:
        print(f"No results found for {city}.")
