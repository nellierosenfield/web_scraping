# Web scraping project using bs4 and books.toscrape.com playground
from bs4 import BeautifulSoup
import requests

books = []
# URl of pages we are scraping with looping
for page_number in range(1, 51):
    url = f"https://books.toscrape.com/catalogue/page-{page_number}.html"

    # GETting page content and storing it into response object
    response = requests.get(url)
    response = response.content

    # Converting response content from binary to html
    soup = BeautifulSoup(response, 'html.parser')

    # We will now obtain three things: the book's rating, title and price

    # First we need to grab the main ol that is the container and then all article tags which contain each book
    ol = soup.find('ol')
    articles = ol.find_all('article', class_='product_pod')

    # Container for our list of books


    # Now we will loop though each article and grab the three things we need
    for article in articles:
        # Book title is located in atl attribute of img tag
        image = article.find('img')
        title = image.attrs['alt']

        # Book rating is located in class attr of p tag
        star = article.find('p')
        star = star['class'][1]

        # Book price is located in class "price_color" of p tag
        price = article.find('p', class_='price_color').text
        price = float(price[1:])

        # Now we will combine them together
        books.append([title, price, star])

