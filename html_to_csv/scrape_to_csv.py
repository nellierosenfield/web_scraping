# Web scraping project using bs4 and books.toscrape.com playground
from bs4 import BeautifulSoup
import pandas as pd
import requests

# Container for our list of books
books = []

for page_number in range(1, 6):
    # URl of pages we are scraping with looping
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

# Now we will work on getting our list of books into a CSV

# Creating dataframe to store list and add columns
df = pd.DataFrame(books, columns=['Title', 'Price', 'Rating'])

# Adding to CSV
df.to_csv("html_to_csv/books.csv")