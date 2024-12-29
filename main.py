from src.scrapers.linkedin_scraper import LinkedInScraper
from src.scrapers.naukri_scraper import NaukriScraper
from src.profile.user_profile import UserProfile
from src.analyzer.job_analyzer import JobAnalyzer
from src.form_filler.application_filler import ApplicationFiller
import json
import time

def load_credentials():
    """Load credentials from config file"""
    try:
        with open('config/credentials.json', 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading credentials: {str(e)}")
        return None

def main():
    # Load credentials
    credentials = load_credentials()
    if not credentials:
        print("Failed to load credentials. Please check config/credentials.json")
        return

    # Initialize components
    user_profile = UserProfile().get_profile()
    linkedin_scraper = LinkedInScraper()
    naukri_scraper = NaukriScraper()
    job_analyzer = JobAnalyzer(user_profile)
    
    all_jobs = []
    
    try:
        # Search for both positions
        search_keywords = ["Java Developer", "Software Engineer"]
        
        # LinkedIn scraping
        print("\nStarting LinkedIn scraping...")
        linkedin_scraper.start_driver()
        linkedin_scraper.login(
            credentials['linkedin']['email'],
            credentials['linkedin']['password']
        )
        for keywords in search_keywords:
            linkedin_scraper.search_jobs(keywords)
            time.sleep(2)
        all_jobs.extend(linkedin_scraper.jobs)
        linkedin_scraper.close()

        # Naukri scraping
        print("\nStarting Naukri scraping...")
        naukri_scraper.start_driver()
        naukri_scraper.login(
            credentials['naukri']['email'],
            credentials['naukri']['password']
        )
        for keywords in search_keywords:
            naukri_scraper.search_jobs(keywords)
            time.sleep(2)
        all_jobs.extend(naukri_scraper.jobs)
        naukri_scraper.close()
        
        # Analyze jobs
        print("\nAnalyzing jobs...")
        analyzed_jobs = job_analyzer.analyze_jobs(all_jobs)
        
        # Generate report
        report_file = job_analyzer.generate_report()
        print(f"\nAnalysis complete! Report saved to: {report_file}")
        
        # Get top matching jobs and apply
        top_jobs = job_analyzer.get_top_jobs(5)
        print("\nAttempting to apply for top 5 matching jobs...")
        
        for job in top_jobs:
            if job['platform'] == 'LinkedIn':
                linkedin_scraper.start_driver()
                filler = ApplicationFiller(linkedin_scraper.driver, user_profile)
                filler.fill_application(job)
                linkedin_scraper.close()
            elif job['platform'] == 'Naukri':
                naukri_scraper.start_driver()
                filler = ApplicationFiller(naukri_scraper.driver, user_profile)
                filler.fill_application(job)
                naukri_scraper.close()
        
        print("\nJob application process completed!")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    
    finally:
        # Make sure browsers are closed
        linkedin_scraper.close()
        naukri_scraper.close()

if __name__ == "__main__":
    main()