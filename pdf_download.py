import requests
from bs4 import BeautifulSoup
import datetime 


def download_pdf(url, file_name):
    response = requests.get(url)
    if response.status_code == 200:
        with open(file_name, "wb") as f:
            f.write(response.content)
    else:
        print(response.status_code)

currentDate = datetime.date.today()
eccles_mosque_url = "https://ecclesmosque.org.uk/"
response = requests.get(eccles_mosque_url)
soup = BeautifulSoup(response.text, 'html.parser')
download_button = soup.find("a",{"class": "em-timetable-download-button"})


download_pdf(download_button.get('href'), str(currentDate) + ".pdf")



