from base64 import encode
from quopri import encodestring
import requests
import os
from bs4 import BeautifulSoup
import datetime 
import smtplib
from os.path import basename
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import ssl

from dotenv import load_dotenv


load_dotenv()
EMAIL_APP_PASSWORD = os.environ.get('EMAIL_APP_PASSWORD')



currentDate = datetime.date.today()
eccles_mosque_url = "https://ecclesmosque.org.uk/"
response = requests.get(eccles_mosque_url)
soup = BeautifulSoup(response.text, 'html.parser')
download_button = soup.find("a",{"class": "em-timetable-download-button"})
eccles_url = download_button.get('href')
pdf_file = str(currentDate) + ".pdf"


def download_pdf():
    response = requests.get(eccles_url)
    if response.status_code == 200:
        with open(pdf_file, "wb") as f:
            f.write(response.content)
    else:
        print(response.status_code)

def email_pdf():
  email_sender_and_reciever= 'mahsinsaifullah@gmail.com'
  second_reciever = 'asma30330@gmail.com'
  subject='Eccles prayer time'
  content = 'Eccles prayer timetable.'
  msg = MIMEMultipart()
  msg['From'] = email_sender_and_reciever
  msg['To'] = email_sender_and_reciever
  msg['Subject'] = subject
  body = MIMEText(content, 'plain')
  msg.attach(body)
  with open(pdf_file, 'r', encoding='latin1') as f:
    part = MIMEApplication(f.read(), Name=basename(pdf_file))
    part['Content-Disposition'] = 'attachment; filename="{}"'.format(basename(pdf_file))
    msg.attach(part)
  context = ssl.create_default_context()
  server = smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context)
  server.login(email_sender_and_reciever, EMAIL_APP_PASSWORD)
  server.send_message(msg, from_addr=email_sender_and_reciever, to_addrs=[email_sender_and_reciever, second_reciever])

 




download_pdf()
email_pdf()



