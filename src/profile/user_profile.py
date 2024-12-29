class UserProfile:
    def __init__(self):
        self.profile_data = {
            'name': 'Aadyant Tripathi',
            'email': 'aadyanttripathi18@gmail.com',
            'phone': '+91 8881298845',
            'location': 'India',
            'links': {
                'portfolio': True,
                'linkedin': True,
                'github': True
            },
            'education': [
                {
                    'degree': 'B.E. Computer Science & Engineering',
                    'school': 'Chandigarh University',
                    'duration': '2021 - 2025'
                },
                {
                    'degree': 'Intermediate',
                    'school': 'City Montessori School',
                    'duration': '2019 - 2020'
                },
                {
                    'degree': 'Matriculation',
                    'school': 'City Montessori School',
                    'duration': '2017 - 2018'
                }
            ],
            'experience': [
                {
                    'title': 'Java Developer',
                    'company': 'Inventory Management System',
                    'duration': 'Jan 2023 - Jan 2024',
                    'highlights': [
                        'Built a scalable system using Java and MySQL with automated CI/CD pipelines via Jenkins and Docker',
                        'Enhanced performance by implementing OOP principles and data structures, improving query execution by 25%',
                        'Collaborated in a team to align solutions with business needs, demonstrating effective teamwork'
                    ]
                }
            ],
            'skills': {
                'languages': ['C/C++ STL', 'Java', 'Python'],
                'web': ['HTML', 'CSS', 'Javascript'],
                'database': ['Java Database Connectivity (JDBC)', 'Structured Data'],
                'technologies': ['Object-Oriented Programming (OOP)', 'Git', 'UI Automation', 'UX']
            }
        }
    
    def get_profile(self):
        return self.profile_data
    
    def update_profile(self, key, value):
        self.profile_data[key] = value