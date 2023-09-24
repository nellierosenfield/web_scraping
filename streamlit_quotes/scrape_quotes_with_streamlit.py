from bs4 import BeautifulSoup
import streamlit as st
import pandas as pd
import requests

# List of tags we'll focus on and creates selectbox in st portal
tag = st.selectbox('Choose a topic', ['love', 'humor', 'life', 'books'])

# Url we are scrapping
url =f"https://quotes.toscrape.com/tag/{tag}/"
response = requests.get(url)

content = BeautifulSoup(response.content, 'html.parser')
quotes = content.find_all('div', class_ = 'quote')

# From each quote container, we get the quote text, author and author page url
for quote in quotes:
    text = quote.find('span', class_ = 'text').text
    author = quote.find('small', class_ = 'author').text
    link = f"https://quotes.toscrape.com{quote.find('a')['href']}"

    # Adds nice green background to displayed text
    st.success(text)

    # Hyperlinks author name to author page link
    st.markdown(f"<a href=\"{link}\">{author}</a>", unsafe_allow_html = True)