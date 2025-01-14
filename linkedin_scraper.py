# This script uses a combination of Selenium and BeautifulSoup as required by the assignment.
# Selenium is used for browser automation tasks like navigating pages, clicking elements, and entering text.
# BeautifulSoup is used to parse the HTML fetched by Selenium for structured data extraction, making it easier
# to extract specific information like profile URLs and images efficiently.

import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd

# Setting up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class LinkedInScraper:
    def __init__(self, chrome_path, driver_path, number_of_results):
        # Initializing the LinkedIn scraper with Chrome driver
        chrome_options = Options()
        chrome_options.binary_location = chrome_path
        service = Service(executable_path=driver_path)
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.wait = WebDriverWait(self.driver, 30)
        self.number_of_results = number_of_results
        logging.info("LinkedIn scraper initialized.")

    def open_page(self, url):
        # Opening the specified URL
        try:
            self.driver.get(url)
            logging.info(f"Page opened: {url}")
        except Exception as e:
            logging.error(f"Error opening page {url}: {e}")

    def interact_with_element(self, selector, text=None, click=False):
        # Interacting with an element: enter text or click
        try:
            element = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
            if text:
                element.send_keys(text)
                logging.info(f"Entered text into: {selector}")
            if click:
                element.click()
                logging.info(f"Clicked element: {selector}")
        except Exception as e:
            logging.error(f"Error interacting with element {selector}: {e}")

    def get_element_html(self, selector):
        # Getting the outer HTML of an element specified by the CSS selector
        try:
            element = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
            logging.info(f"HTML retrieved for element: {selector}")
            return element.get_attribute('outerHTML')
        except Exception as e:
            logging.error(f"Error getting HTML from {selector}: {e}")
            return ""

    def extract_profile_data(self, ul_html):
        # Extracting profile data including profile URL and image URL from HTML
        soup = BeautifulSoup(ul_html, 'html.parser')
        profiles = soup.find_all('li', class_='pserp-layout__profile-result-list-item')[:self.number_of_results]

        profile_data = []
        for profile in profiles:
            try:
                title_element = profile.find('h3', class_='base-search-card__title')
                title = title_element.get_text(strip=True).split()
                first_name = title[0]
                last_name = title[-1]

                # If the name has more than two words
                if len(title) > 2:
                    first_name= " ".join(title[:-1])  # All parts except the last go into the first name
                    last_name = title[-1]  # The last part is the last name
                    
                # Extracting the Profile URL
                profile_link_tag = title_element.find_parent('a', href=True)
                profile_url = profile_link_tag['href'] if profile_link_tag else ""

                # Extracting the Image URL
                image_tag = profile.find('img', attrs={'data-ghost-classes': 'artdeco-entity-image--ghost'})
                if image_tag:
                    image_url = image_tag.get('src') or image_tag.get('data-ghost-url', '')
                else:
                    image_url = ""

                subtitle = profile.find('h4', class_='base-search-card__subtitle')
                subtitle = subtitle.get_text(strip=True) if subtitle else ""

                location = profile.find('p', class_='people-search-card__location')
                location = location.get_text(strip=True) if location else ""

                company = profile.find_all('span', class_='entity-list-meta__entities-list')
                company = company[0].get_text(strip=True) if company else ""

                college = (profile.find_all('span', class_='entity-list-meta__entities-list')[1]
                           .get_text(strip=True).split(',')[0] if len(profile.find_all('span', 'entity-list-meta__entities-list')) > 1 else "")

                # Appending all the data to the list
                data_dict = {
                    "First Name": first_name,
                    "Last Name": last_name,
                    "Profile URL": profile_url,
                    "Image URL": image_url,
                    "Profession": subtitle,
                    "Location": location,
                    "Company": company,
                    "Education": college
                }
                profile_data.append(data_dict)
                logging.info(f"Extracted data for: {first_name} {last_name}")
            except Exception as e:
                logging.error(f"Error extracting profile data: {e}")

        return profile_data

    def export_to_csv(self, data, file_path):
        # Exporting the data to a CSV file
        try:
            df = pd.DataFrame(data)
            df.to_csv(file_path, index=False)
            logging.info(f"Data exported to {file_path} successfully.")
        except Exception as e:
            logging.error(f"Error exporting data to CSV: {e}")

    def close(self):
        # Closing the browser
        try:
            self.driver.quit()
            logging.info("Browser closed successfully.")
        except Exception as e:
            logging.error(f"Error closing the browser: {e}")

if __name__ == "__main__":
    # Defining the paths
    CHROME_PATH = r"C:\\Users\\hp\\Documents\\Assignment_Ecowiser\\chrome-win64\\chrome.exe"
    DRIVER_PATH = r"C:\\Users\\hp\\Documents\\Assignment_Ecowiser\\driver\\chromedriver.exe"
    URL = "https://in.linkedin.com/jobs/search?position=1&pageNum=1"
    OUTPUT_FILE = "linkedin_profiles.csv"

    first_name = input("Enter first name: ").lower()
    last_name = input("Enter last name: ").lower()
    number_of_results = 10  # Number of results to fetch

    scraper = LinkedInScraper(CHROME_PATH, DRIVER_PATH, number_of_results)

    try:
        scraper.open_page(URL)

        # Defining the selectors
        close_button_selector = "button[data-tracking-control-name='public_jobs_contextual-sign-in-modal_modal_dismiss']"
        jobs_button_selector = "button[data-tracking-control-name='public_jobs_switcher-tabs-placeholder']"
        people_button_selector = "button[data-tracking-control-name='public_jobs_switcher-tabs-people-search-switcher']"
        first_name_input_selector = "input[data-tracking-control-name='public_jobs_people-search-bar_first-name_dismissable-input']"
        last_name_input_selector = "input[data-tracking-control-name='public_jobs_people-search-bar_last-name_dismissable-input']"
        search_button_selector = "button[data-tracking-control-name='public_jobs_people-search-bar_base-search-bar-search-submit']"
        ul_selector = ".serp-page__results-list ul"

        # Interacting with the page
        scraper.interact_with_element(close_button_selector, click=True)
        scraper.interact_with_element(jobs_button_selector, click=True)
        scraper.interact_with_element(people_button_selector, click=True)
        scraper.interact_with_element(first_name_input_selector, text=first_name)
        scraper.interact_with_element(last_name_input_selector, text=last_name)
        scraper.interact_with_element(search_button_selector, click=True)

        ul_html = scraper.get_element_html(ul_selector)
        profile_data = scraper.extract_profile_data(ul_html)
        scraper.export_to_csv(profile_data, OUTPUT_FILE)

    except Exception as e:
        logging.error(f"An error occurred: {e}")

    finally:
        scraper.close()