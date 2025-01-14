# LinkedIn Profile Scraper - Web Scraping Script

## Overview
This project implements a LinkedIn profile scraper using **Selenium** and **BeautifulSoup** to extract data from LinkedIn based on a user's first and last name. The script fetches detailed information from LinkedIn profiles, including:

- First Name
- Last Name
- Profile URL
- Image URL
- Profession
- Location
- Company
- Education

The script is designed to extract information about the first 5 relevant search result profiles and save this data into a CSV file.

## Project Requirements

### Python Libraries:
- `selenium`
- `beautifulsoup4`
- `pandas`
- `logging`

### Tools:
- Google Chrome
- Chrome WebDriver (`chromedriver`)

### Installation

To set up the project, follow these steps:

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/linkedin-profile-scraper.git
   cd linkedin-profile-scraper
   ```

2. **Create and activate a virtual environment (optional but recommended):**

    ```bash
    python -m venv .venv
    source .venv/bin/activate   # For MacOS/Linux
    .venv\Scripts\activate      # For Windows
    ```

3. **Install required dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Download the correct version of ChromeDriver**
    
    - Download the ChromeDriver from this [link](https://drive.google.com/drive/folders/1hR5z5BOMQTojkhMDefzoXiUf7hH2aKc-?usp=drive_link).

5. **Download the corresponding version of Google Chrome:**

    - Download the suitable version of Google Chrome from this [link](https://drive.google.com/drive/folders/1_b5mstmPRWW2GaXAjylFFNw-ZXyx7YAk?usp=drive_link).

6. **Set the path for Chrome and ChromeDriver:**

    - Specify the path for your `chrome.exe` and `chromedriver.exe` in the script.

---

## Script Details

This script takes the following input:

- **First Name** (e.g., "John")
- **Last Name** (e.g., "Doe")

## Running the Script

To run the script, execute the following command in your terminal:

```bash
python linkedin_scraper.py
```

It then navigates through LinkedIn, performs a search with the given names, and extracts relevant profile details for the first 5 profiles.

### The script follows these steps:

1. **Open LinkedIn** - The URL is set to the job search page, and the browser is automated using Selenium.
2. **Interact with the page** - Using Selenium, it interacts with various page elements such as buttons, search input fields, etc.
3. **Extract Profile Data** - The page content is fetched using BeautifulSoup, and the necessary details (name, location, company, etc.) are extracted.
4. **Export Data** - The collected data is saved into a CSV file named `linkedin_profiles.csv`.

---

### Example Input

```bash
Enter first name: John
Enter last name: Doe
```

## Logging

The script logs important actions, including:

- Page loading
- Profile data extraction
- Errors and exceptions

Logs are saved with timestamps for better debugging.