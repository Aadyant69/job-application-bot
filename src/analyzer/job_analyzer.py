from difflib import SequenceMatcher
import re
from datetime import datetime

class JobAnalyzer:
    def __init__(self, user_profile):
        self.user_profile = user_profile
        self.analyzed_jobs = []
        self.target_positions = ['java developer', 'software engineer']
        self.target_levels = ['internship', 'entry level', 'fresher', '0-2 years', 
                            'graduate', 'trainee', 'junior']

    def _calculate_job_score(self, job):
        """Calculate how well the job matches the user's profile"""
        score = {
            'skills_match': 0,
            'position_match': 0,
            'level_match': 0,
            'location_match': 0,
            'analysis': {}
        }

        # Convert job description and title to lowercase for better matching
        job_text = f"{job.get('title', '')} {job.get('description', '')}".lower()
        job_title = job.get('title', '').lower()

        # Skills matching
        user_skills = (
            self.user_profile['skills']['languages'] +
            self.user_profile['skills']['technologies'] +
            self.user_profile['skills']['web']
        )
        matched_skills = []
        for skill in user_skills:
            if skill.lower() in job_text:
                matched_skills.append(skill)
                score['skills_match'] += 1

        # Position matching
        for position in self.target_positions:
            if position in job_title:
                score['position_match'] = 10
                break

        # Experience level matching
        experience_text = f"{job_text} {job.get('experience_required', '').lower()}"
        for level in self.target_levels:
            if level in experience_text:
                score['level_match'] = 10
                break

        # Location matching
        user_location = self.user_profile.get('location', '').lower()
        job_location = job.get('location', '').lower()
        if user_location in job_location or job_location in user_location:
            score['location_match'] = 10

        # Calculate total score (weighted average)
        total_score = (
            (score['skills_match'] * 3) +
            (score['position_match'] * 3) +
            (score['level_match'] * 3) +
            (score['location_match'] * 1)
        ) / 10

        # Prepare analysis
        score['analysis'] = {
            'matched_skills': matched_skills,
            'position_match': bool(score['position_match']),
            'level_match': bool(score['level_match']),
            'location_match': bool(score['location_match']),
            'is_entry_level': bool(score['level_match'])
        }
        score['total_score'] = round(total_score, 2)

        return score

    def filter_entry_level_jobs(self, jobs):
        """Pre-filter to only include entry-level positions"""
        filtered_jobs = []
        for job in jobs:
            job_text = f"{job.get('title', '')} {job.get('description', '')} {job.get('experience_required', '')}".lower()
            
            # Check if it's an appropriate position
            is_target_position = any(position in job.get('title', '').lower() 
                                   for position in self.target_positions)
            
            # Check if it's entry level
            is_entry_level = any(level in job_text for level in self.target_levels)
            
            if is_target_position and is_entry_level:
                filtered_jobs.append(job)
        
        return filtered_jobs

    def analyze_jobs(self, jobs):
        """Analyze and score jobs based on profile match"""
        print("\nAnalyzing jobs for profile match...")
        
        # First filter for entry-level positions
        filtered_jobs = self.filter_entry_level_jobs(jobs)
        print(f"Found {len(filtered_jobs)} entry-level positions out of {len(jobs)} total jobs")
        
        # Then analyze the filtered jobs
        for job in filtered_jobs:
            job_score = self._calculate_job_score(job)
            analyzed_job = {
                **job,
                'score': job_score['total_score'],
                'analysis': job_score['analysis']
            }
            self.analyzed_jobs.append(analyzed_job)
        
        # Sort jobs by score
        self.analyzed_jobs.sort(key=lambda x: x['score'], reverse=True)
        return self.analyzed_jobs

    def get_top_jobs(self, limit=10):
        """Get top matching jobs"""
        return self.analyzed_jobs[:limit]

    def generate_report(self, filename=None):
        """Generate a detailed report of job matches"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"job_analysis_{timestamp}.txt"

        with open(filename, 'w', encoding='utf-8') as f:
            f.write("Job Analysis Report\n")
            f.write("=================\n\n")
            
            for idx, job in enumerate(self.analyzed_jobs, 1):
                f.write(f"#{idx} Job: {job['title']}\n")
                f.write(f"Company: {job['company']}\n")
                f.write(f"Location: {job['location']}\n")
                f.write(f"Match Score: {job['score']}/10\n")
                f.write("\nAnalysis:\n")
                f.write(f"- Matched Skills: {', '.join(job['analysis']['matched_skills'])}\n")
                f.write(f"- Position Match: {'Yes' if job['analysis']['position_match'] else 'No'}\n")
                f.write(f"- Entry Level: {'Yes' if job['analysis']['is_entry_level'] else 'No'}\n")
                f.write(f"- Location Match: {'Yes' if job['analysis']['location_match'] else 'No'}\n")
                f.write(f"Platform: {job['platform']}\n")
                f.write(f"Apply Link: {job['link']}\n")
                f.write("\n" + "="*50 + "\n\n")

        return filename