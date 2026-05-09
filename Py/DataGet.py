import requests
from bs4 import BeautifulSoup

url = 'https://www.lavozdesanjusto.com.ar/categoria/policiales'

response = requests.get(url)

html =  response.text

soup = BeautifulSoup(html, 'html.parser')

for h2 in soup.find_all('h2'):
    print(h2.get_text(strip=True))


