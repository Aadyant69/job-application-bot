import json
import os

class Config:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.credentials = self._load_credentials()
        
    def _load_credentials(self):
        cred_path = os.path.join(self.base_dir, 'config', 'credentials.json')
        with open(cred_path, 'r') as f:
            return json.load(f)
        
    @property
    def linkedin_credentials(self):
        return self.credentials.get('linkedin', {})
    
    @property
    def naukri_credentials(self):
        return self.credentials.get('naukri', {})