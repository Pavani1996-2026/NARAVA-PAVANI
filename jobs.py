import requests
from bs4 import BeautifulSoup
import smtplib
from email.message import EmailMessage
from datetime import datetime

EMAIL = "krishnapavani1996@gmail.com"
SENDER = "yourgmail@gmail.com"
APP_PASSWORD = "your_gmail_app_password"

KEYWORDS = [
    "entry level data analyst",
    "junior data analyst",
    "graduate data analyst",
    "crm data analyst",
    "reporting analyst"
]INDEED_URL = "https://uk.indeed.com/jobs?q={}&fromage=1"

def scrape_indeed(keyword):
    jobs = []
    url = INDEED_URL.format(keyword.replace(" ", "+"))
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")

    for job in soup.find_all("a"):
        if "/rc/clk" in str(job.get("href")):
            title = job.text.strip()
            link = "https://uk.indeed.com" + job.get("href")
            jobs.append((title, link))

    return jobs[:10]
def send_email(all_jobs):
    msg = EmailMessage()
    msg["Subject"] = f"Daily Entry-Level Data Jobs - {datetime.today().date()}"
    msg["From"] = SENDER
    msg["To"] = EMAIL

    content = ""

    for keyword in KEYWORDS:
        jobs = scrape_indeed(keyword)
        for title, link in jobs:
            content += f"{title}\n{link}\n\n"

    if not content:
        content = "No new jobs found today."

    msg.set_content(content)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(SENDER, APP_PASSWORD)
        smtp.send_message(msg)

if __name__ == "__main__":
    send_email(KEYWORDS)
