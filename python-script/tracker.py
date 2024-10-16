import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json
import os
from dotenv import load_dotenv

CAREERS_URLS = ['https://apply.workable.com/verbinteractive/?lng=en#jobs']

DATA_FILE = 'jobs.json'

EMAIL_SENDER = 'zoowadi.gaming@gmail.com'
EMAIL_RECEIVER = 'parwatkunwar08@gmail.com'
EMAIL_SUBJECT = 'New Job Posting @ Verb Interactive.'
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')

def fetch_job_postings(urls):
    jobs = []
    for url in urls:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Assuming job postings are contained within a div with id='jobs'
        job_elements = soup.find_all('div', class_='job')  # Adjust this based on actual HTML structure
        for job_element in job_elements:
            title = job_element.find('h2').text.strip()
            location = job_element.find('div', class_='location').text.strip() if job_element.find('div', class_='location') else 'No location'
            link = job_element.find('a')['href']

            jobs.append({
                'title': title,
                'location': location,
                'link': link
            })

    return jobs
