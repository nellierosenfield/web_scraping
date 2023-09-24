from bs4 import BeautifulSoup
import streamlit as st
import pandas as pd
import requests
import re

# List of tags we'll focus on and creates selectbox in st portal
tag = st.selectbox('Choose a topic', ['love', 'humor', 'life', 'books'])

csv_button = st.button("Export to CSV")

# Url we are scrapping
url =f"https://quotes.toscrape.com/tag/{tag}/"
response = requests.get(url)

content = BeautifulSoup(response.content, 'html.parser')
quotes = content.find_all('div', class_ = 'quote')

quote_file = []

# From each quote container, we get the quote text, author and author page url
for quote in quotes:
    text = quote.find('span', class_ = 'text').text
    blurb = re.sub("[“”]", "", text) # removes annoying quotes taken from html page
    author = quote.find('small', class_ = 'author').text
    link = f"https://quotes.toscrape.com{quote.find('a')['href']}"

    # Adds nice green background to displayed text
    st.success(blurb) # adds quotes only for display

    # Hyperlinks author name to author page link
    st.markdown(f"<a href=\"{link}\">{author}</a>", unsafe_allow_html = True)

    # adding contents to list for pushing to csv file
    quote_file.append([blurb, author, link])

# will export quotes to csv when csv_button is pushed
if csv_button:
    try:
        df = pd.DataFrame(quote_file)
        df.to_csv('exported_quotes.csv', index = False, header = ['Quote', 'Author', 'Biography'], encoding = "utf-8")
    except:
        st.write('Exporting...')