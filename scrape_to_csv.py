# Web scraping project using bs4 and books.toscrape.com playground
from bs4 import BeautifulSoup
import requests

# URl of page we are scraping
url = "https://books.toscrape.com/catalogue/page-1.html"

# GETting page content and storing it into response object
response = requests.get(url)
response = response.content

# Converting response content from binary to html
soup = BeautifulSoup(response, 'html.parser')