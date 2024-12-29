from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import os

class ApplicationFiller:
    def __init__(self, driver, user_profile):
        self.driver = driver
        self.user_profile = user_profile
        self.wait = WebDriverWait(self.driver, 10)
        
    def fill_application(self, job):
        """Main method to fill job application"""
        try:
            # Check if job is entry level
            if not self._is_entry_level(job):
                print(f"Skipping {job['title']} - Not an entry level position")
                return False
                
            print(f"\nAttempting to fill application for: {job['title']} at {job['company']}")
            
            # Navigate to job application page
            self.driver.get(job['link'])
            time.sleep(3)
            
            if 'linkedin.com' in job['link']:
                return self._fill_linkedin_application()
            elif 'naukri.com' in job['link']:
                return self._fill_naukri_application()
            else:
                print("Unsupported application platform")
                return False
                
        except Exception as e:
            print(f"Error filling application: {str(e)}")
            return False

    def _is_entry_level(self, job):
        """Check if the job is entry level"""
        entry_level_keywords = [
            'internship', 'entry level', 'fresher', '0-2 years',
            'graduate', 'trainee', 'junior'
        ]
        
        job_text = f"{job.get('title', '')} {job.get('description', '')} {job.get('experience_required', '')}".lower()
        
        return any(keyword in job_text for keyword in entry_level_keywords)

    def _fill_linkedin_application(self):
        """Fill LinkedIn job application"""
        try:
            # Find and click apply button
            apply_button = self.wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "jobs-apply-button"))
            )
            apply_button.click()
            time.sleep(2)

            # Fill basic information
            self._fill_linkedin_form()
            
            # Handle resume upload
            self._upload_resume()
            
            # Handle additional questions
            self._handle_additional_questions()
            
            # Submit application (commented out for safety)
            submit_button = self.driver.find_element(By.CSS_SELECTOR, "button[aria-label='Submit application']")
            submit_button.click()
            
            print("LinkedIn application filled successfully")
            return True

        except Exception as e:
            print(f"Error in LinkedIn application: {str(e)}")
            return False

    def _fill_naukri_application(self):
        """Fill Naukri job application"""
        try:
            # Find and click apply button
            apply_button = self.wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "apply-button"))
            )
            apply_button.click()
            time.sleep(2)

            # Fill basic information
            self._fill_naukri_form()
            
            # Handle resume upload if needed
            self._upload_resume()
            
            # Submit application (commented out for safety)
            submit_button = self.driver.find_element(By.CSS_SELECTOR, "button.submit-application")
            submit_button.click()
            
            print("Naukri application filled successfully")
            return True

        except Exception as e:
            print(f"Error in Naukri application: {str(e)}")
            return False

    def _fill_linkedin_form(self):
        """Fill common LinkedIn form fields"""
        try:
            # Map of common field identifiers and their values
            field_mapping = {
                'first-name': self.user_profile['name'].split()[0],
                'last-name': self.user_profile['name'].split()[-1],
                'email': self.user_profile['email'],
                'phone': self.user_profile['phone'],
                'location': self.user_profile['location']
            }

            # Fill each field if found
            for field_id, value in field_mapping.items():
                try:
                    field = self.driver.find_element(By.ID, field_id)
                    field.clear()
                    field.send_keys(value)
                except:
                    continue

        except Exception as e:
            print(f"Error filling LinkedIn form: {str(e)}")

    def _fill_naukri_form(self):
        """Fill common Naukri form fields"""
        try:
            # Map of common field identifiers and their values
            field_mapping = {
                'name': self.user_profile['name'],
                'email': self.user_profile['email'],
                'mobile': self.user_profile['phone'],
                'location': self.user_profile['location']
            }

            # Fill each field if found
            for field_id, value in field_mapping.items():
                try:
                    field = self.driver.find_element(By.NAME, field_id)
                    field.clear()
                    field.send_keys(value)
                except:
                    continue

        except Exception as e:
            print(f"Error filling Naukri form: {str(e)}")

    def _upload_resume(self):
        """Handle resume upload if required"""
        try:
            # Path to your resume file
            resume_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
                                     'resources', 'resume.pdf')
            
            # Find upload button/input
            upload_input = self.driver.find_element(By.CSS_SELECTOR, "input[type='file']")
            upload_input.send_keys(resume_path)
            time.sleep(2)
            
            print("Resume uploaded successfully")
            
        except Exception as e:
            print(f"Error uploading resume: {str(e)}")

    def _handle_additional_questions(self):
        """Handle any additional application questions"""
        try:
            # Find all question containers
            questions = self.driver.find_elements(By.CLASS_NAME, "application-question")
            
            for question in questions:
                question_text = question.find_element(By.CLASS_NAME, "question-text").text
                
                # Handle different question types based on your profile
                if "years of experience" in question_text.lower():
                    answer = "1"  # Based on your profile
                elif "willing to relocate" in question_text.lower():
                    answer = "Yes"
                elif "expected salary" in question_text.lower():
                    answer = "As per industry standards"
                else:
                    answer = "Yes"  # Default positive response
                
                # Find and fill answer field
                try:
                    answer_field = question.find_element(By.TAG_NAME, "input")
                    answer_field.send_keys(answer)
                except:
                    continue
                
        except Exception as e:
            print(f"Error handling additional questions: {str(e)}")