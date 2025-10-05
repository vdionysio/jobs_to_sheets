import ezsheets
import requests
import os
# import re
# import json
from dotenv import load_dotenv

load_dotenv()
X_API_KEY = os.getenv("X_API_KEY")
SHEETS_URL = os.getenv("SHEETS_URL")
JSEARCH_URL = "https://api.openwebninja.com/jsearch/search"
headers = {"x-rapidapi-host": "jsearch.p.rapidapi.com", "x-api-key": X_API_KEY}

def get_jobs_by_key(key):
    querystring = {
      "query": key,
      "country": "br",
      "work_from_home": "true"
    }
    jobs = []
    data = requests.get(JSEARCH_URL, headers=headers, params=querystring).json()['data']

    for job in data:
        description = job['job_description']
        title = job['job_title']
        # extract_email_pattern = r"\S+@\S+\.\S+"
        # emails = re.findall(extract_email_pattern, description)
        if ('junior' in title.lower() or 'estagio' in title.lower()):
            jobs.append(job)

    return jobs

jobs = get_jobs_by_key('software') + get_jobs_by_key('dados') + get_jobs_by_key('programador') + get_jobs_by_key('tecnologia') + get_jobs_by_key('software')


sheet = ezsheets.Spreadsheet(SHEETS_URL)[0]
if (not sheet['A1']):
    sheet['A1'] = 'Título' # job_title
    sheet['B1'] = 'link' # job_apply_link
    
for i in range(len(jobs)):
    sheet[1, i + 2] = jobs[i]['job_title']
    sheet[2, i + 2] = jobs[i]['job_apply_link']