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



  for url in urls:
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    jobs = []
    for job_element in soup.find_all('div', id='jobs'):
      title


def send_email(new_jobs):
