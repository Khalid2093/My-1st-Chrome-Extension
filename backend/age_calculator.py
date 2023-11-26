from datetime import datetime

class AgeCalculator:
    def __init__(self, education_year=None, job_start_year=None):
        self.education_year = education_year
        self.job_start_year = job_start_year

    def calculate_age(self):
        current_year = datetime.now().year

        if self.education_year:
            
            return current_year - self.education_year + 18
        elif self.job_start_year:
            
            return current_year - self.job_start_year + 22
        else:
            
            return None
