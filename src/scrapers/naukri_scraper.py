from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import json

class NaukriScraper:
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
        """Login to Naukri"""
        try:
            print("Attempting to log in to Naukri...")
            self.driver.get("https://www.naukri.com/nlogin/login")
            time.sleep(2)

            # Find and fill email
            email_field = self.driver.find_element(By.ID, "usernameField")
            email_field.send_keys(email)

            # Find and fill password
            password_field = self.driver.find_element(By.ID, "passwordField")
            password_field.send_keys(password)

            # Click login button
            login_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Login')]")
            login_button.click()

            time.sleep(5)
            print("Successfully logged in to Naukri")

        except Exception as e:
            print(f"Error logging in to Naukri: {str(e)}")
            raise

    def search_jobs(self, keywords):
        """Search for jobs using keywords"""
        try:
            print(f"Searching for {keywords} jobs...")
            search_query = "-".join(keywords.split())
            # Add experience level to URL
            url = f"https://www.naukri.com/{search_query}-jobs-in-india?experience=0"
            self.driver.get(url)
            time.sleep(3)

            # Scroll to load more jobs
            self._scroll_page()

            # Extract job listings
            job_cards = self.driver.find_elements(By.CLASS_NAME, "jobTuple")
            
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
            print(f"Error in Naukri job search: {str(e)}")

    def _extract_job_data(self, card):
        """Extract data from a job card"""
        try:
            # Extract basic information
            title = card.find_element(By.CLASS_NAME, "title").text
            company = card.find_element(By.CLASS_NAME, "companyInfo").text
            location = card.find_element(By.CLASS_NAME, "location").text
            
            # Get the job link
            link = card.find_element(By.CSS_SELECTOR, "a.title").get_attribute("href")

            # Try to get experience requirement
            try:
                experience = card.find_element(By.CLASS_NAME, "experience").text
            except:
                experience = "Experience not specified"

            # Try to get salary info
            try:
                salary = card.find_element(By.CLASS_NAME, "salary").text
            except:
                salary = "Salary not specified"

            return {
                'title': title,
                'company': company,
                'location': location,
                'link': link,
                'experience_required': experience,
                'salary': salary,
                'platform': 'Naukri'
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