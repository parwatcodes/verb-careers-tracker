import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json
import os
from dotenv import load_dotenv

CAREERS_URLS = ['https://apply.workable.com/verbinteractive/?lng=en#jobs']
load_dotenv()

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

        job_elements = soup.find_all('li', { 'data-ui': 'job' })

        for job_element in job_elements:
            title = job_element.find('h3', {'data-ui': 'job-title'}).text.strip()
            location = job_element.find('div', {'data-ui': 'job-location'}).text.strip() if job_element.find('div', {'data-ui': 'job-location'}) else 'No location'
            link = job_element.find('a')['href']
            posted_on = job_element.find('small', {'data-ui': 'job-posted'}).text.strip()
            department = job_element.find('span', {'data-ui': 'job-department'}).text.strip() if job_element.find('span', {'data-ui': 'job-department'}) else 'No department'
            job_type = job_element.find('span', {'data-ui': 'job-type'}).text.strip() if job_element.find('span', {'data-ui': 'job-type'}) else 'No job type'

            jobs.append({
                'title': title,
                'location': location,
                'link': link,
                'posted_on': posted_on,
                'department': department,
                'job_type': job_type
            })

    return jobs

def load_saved_jobs():
  if os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'r') as file:
      return json.load(file)
  return []

def save_jobs(jobs):
  with open(DATA_FILE, 'w') as file:
    json.dump(jobs, file, indent=4)

def find_new_jobs(jobs, saved_jobs):
  return [job for job in jobs if job not in saved_jobs]

def send_email(new_jobs):
  msg = MIMEMultipart()
  msg['From'] = EMAIL_SENDER
  msg['To'] = EMAIL_RECEIVER
  msg['Subject'] = EMAIL_SUBJECT

  body = "New job postings at Verb Interactive:\n\n"

  for job in new_jobs:
    body += f"Title: {job['title']}\nLocation: {job['location']}\nLink: {job['link']}\n\n"

  msg.attach(MIMEText(body, 'plain'))

  with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
    server.starttls()
    server.login(EMAIL_SENDER, EMAIL_PASSWORD)
    server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())

if __name__ == "__main__":
  saved_jobs = load_saved_jobs()
  current_jobs = fetch_job_postings(CAREERS_URLS)
  new_jobs = find_new_jobs(current_jobs, saved_jobs)

  if new_jobs:
    send_email(new_jobs)
    save_jobs(current_jobs)
    print("New jobs found and email sent!")
  else:
    print("No new jobs found.")
