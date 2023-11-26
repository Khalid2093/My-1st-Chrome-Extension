from flask import Flask, jsonify, request
from age_calculator import AgeCalculator
from datetime import datetime
import json
import os

app = Flask(__name__)

PROFILES_DIR = 'profiles_data'

def load_profiles():
    profiles = []
    for filename in os.listdir(PROFILES_DIR):
        if filename.endswith('.json'):
            filepath = os.path.join(PROFILES_DIR, filename)
            with open(filepath, 'r', encoding='utf-8') as file:
                profile_data = json.load(file)
                profiles.append(profile_data)
    return profiles

profiles = load_profiles()


def extract_education_and_experience(profile):
    education_entries = profile.get("member_education_collection", [])
    experience_entries = profile.get("member_experience_collection", [])

    if(not education_entries and not experience_entries):
        return None, None
    
    def get_date_from(x):
        date_from = x.get("date_from")
        
        if date_from and isinstance(date_from, str):
            last_word = date_from.split()[-1]
            
            try:
                return int(last_word)
            except ValueError:
                # Actually we don't care if the last word is not an integer
                pass
        
        return datetime.now().year

    earliest_education = min(education_entries, key=get_date_from, default=None)
    education_year = get_date_from(earliest_education) if earliest_education else None
    
    earliest_experience = min(experience_entries, key=get_date_from, default=None)
    job_start_year = get_date_from(earliest_experience) if earliest_experience else None
    
    return education_year, job_start_year


@app.route('/profiles', methods=['GET'])
def get_profiles():
    return jsonify(profiles)

@app.route('/age', methods=['GET'])
def get_age():
    profile_name = request.args.get('name')
    profile = next((p for p in profiles if p["name"] == profile_name), None)
    
    if profile:
        education_year, job_start_year = extract_education_and_experience(profile)
        if not education_year and not job_start_year:
            return jsonify({"age": "Not enough information"})
        calculator = AgeCalculator(
            education_year=education_year,
            job_start_year=job_start_year
        )
        age = calculator.calculate_age()
        return jsonify({"age": age})
    else:
        return jsonify({"error": "Profile not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)



































# from flask import Flask, jsonify, request
# from age_calculator import AgeCalculator
# import json
# import os

# app = Flask(__name__)

# # Assuming your JSON files are in a directory named 'profiles_data'
# PROFILES_DIR = 'testData'

# def load_profiles():
#     profiles = []
#     for filename in os.listdir(PROFILES_DIR):
#         if filename.endswith('.json'):
#             filepath = os.path.join(PROFILES_DIR, filename)
#             with open(filepath, 'r', encoding='utf-8') as file:
#                 profile_data = json.load(file)
#                 profiles.append(profile_data)
#     return profiles

# # Load profiles at the start of the application
# profiles = load_profiles()

# @app.route('/profiles', methods=['GET'])
# def get_profiles():
#     return jsonify(profiles)

# @app.route('/age', methods=['GET'])
# def get_age():
#     profile_name = request.args.get('name')
#     profile = next((p for p in profiles if p["name"] == profile_name), None)

#     if profile:
#         calculator = AgeCalculator(
#             education_year=profile.get("education_year"),
#             job_start_year=profile.get("job_start_year")
#         )
#         age = calculator.calculate_age()
#         return jsonify({"age": age})
#     else:
#         return jsonify({"error": "Profile not found"}), 404

# if __name__ == '__main__':
#     app.run(debug=True)
