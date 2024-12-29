from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import json

class LinkedInScraper:
    def __init__(self):
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_argument('--disable-gpu')
        self.chrome_options.add_argument('--no-sandbox')
        self.chrome_options.add_argument('--disable-dev-shm-usage')
        self.driver = None
        self.jobs = []

    def start_driver(self):
        """Initialize the Chrome driver"""
        self.driver = webdriver.Chrome(options=self.chrome_options)
        self.driver.maximize_window()

    def login(self, email, password):
        """Login to LinkedIn"""
        try:
            print("Attempting to log in to LinkedIn...")
            self.driver.get("https://www.linkedin.com/login")
            time.sleep(2)

            # Find and fill email
            email_field = self.driver.find_element(By.ID, "username")
            email_field.send_keys(email)

            # Find and fill password
            password_field = self.driver.find_element(By.ID, "password")
            password_field.send_keys(password)

            # Click login button
            login_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            login_button.click()

            time.sleep(5)
            print("Successfully logged in to LinkedIn")

        except Exception as e:
            print(f"Error logging in to LinkedIn: {str(e)}")
            raise

    def search_jobs(self, keywords):
        """Search for jobs using keywords"""
        try:
            print(f"Searching for {keywords} jobs...")
            # Add entry level filter to URL
            search_query = "+".join(keywords.split())
            url = f"https://www.linkedin.com/jobs/search?keywords={search_query}&f_E=1%2C2&location=India"
            self.driver.get(url)
            time.sleep(3)

            # Scroll to load more jobs
            self._scroll_page()

            # Extract job listings
            job_cards = self.driver.find_elements(By.CLASS_NAME, "jobs-search-results__list-item")
            
            for card in job_cards[:10]:  # Limit to first 10 jobs for testing
                try:
                    job_data = self._extract_job_data(card)
                    if job_data:
                        self.jobs.append(job_data)
                        print(f"Found job: {job_data['title']} at {job_data['company']}")

                except Exception as e:
                    print(f"Error extracting job card data: {str(e)}")
                    continue

        except Exception as e:
            print(f"Error in LinkedIn job search: {str(e)}")

    def _extract_job_data(self, card):
        """Extract data from a job card"""
        try:
            # Click on the card to load details
            card.click()
            time.sleep(2)

            # Extract basic information
            title = card.find_element(By.CSS_SELECTOR, "h3.job-card-list__title").text
            company = card.find_element(By.CSS_SELECTOR, "h4.job-card-container__company-name").text
            location = card.find_element(By.CSS_SELECTOR, "span.job-card-container__metadata-item").text
            
            # Get the job link
            link = card.find_element(By.CSS_SELECTOR, "a.job-card-list__title").get_attribute("href")

            # Try to get job description
            try:
                description = self.driver.find_element(
                    By.CLASS_NAME, "jobs-description__content"
                ).text
            except:
                description = "Description not available"

            return {
                'title': title,
                'company': company,
                'location': location,
                'link': link,
                'description': description,
                'platform': 'LinkedIn'
            }

        except Exception as e:
            print(f"Error extracting job data: {str(e)}")
            return None

    def _scroll_page(self):
        """Scroll the page to load more job listings"""
        SCROLL_PAUSE_TIME = 2
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        for _ in range(3):  # Scroll 3 times
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(SCROLL_PAUSE_TIME)
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    def close(self):
        """Close the browser"""
        if self.driver:
            self.driver.quit()