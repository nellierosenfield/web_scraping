from nltk.tokenize import word_tokenize
from bs4 import BeautifulSoup
import pandas as pd
import requests
import nltk
nltk.download('stopwords')
nltk.download('punkt')

# For this analyzer, we will be checking for the following:
#     - Are there any warnings?
#     - Is there a title and meta description?
#     - Are there are enough header tags, especially h1?
#     - Do images have atl tags for accessibility?
#     - Do the keywords match or relate to the page title?

def seo_analyzer(url):
    response = requests.get(url).text

    soup = BeautifulSoup(response, 'html.parser')

    not_found = [] # What's not found on the site
    found = [] # Items present on the site
    keywords = [] # if present, keywords for optimizing

    # Is there a title and meta description?
    title = soup.find('title').text
    if title:
        found.append(f"Title: {title} (size {len(title)})")
    else:
        not_found.append('Title not found! Please add a title to your site')

    meta_desc = soup.find('meta', attrs = {'name': 'description'})['content']
    if meta_desc:
        found.append(f"Meta Description: {meta_desc}")
    else:
        not_found.append('Meta description not found! Please add a meta description to your site.')

    # Are there are enough header tags, especially h1?
    headings = ['h1', 'h2', 'h3']
    heading_tags = []
    for heading in soup.find_all(headings):
        found.append(f"{heading.name} --> {heading.text.strip()}")
        heading_tags.append(heading.name)

    if 'h1' not in heading_tags:
        not_found.append('No h1 tags found! Please add at least one (1) h1 tag to your site.')

    # Do images have atl tags for accessibility?
    for image in soup.find_all('img', alt = ''):
        not_found.append(f"Warning! This image does not contain an alt: {image}")
    
    seo_report(url, found, not_found)

def seo_report(url, found, not_found):
    print(f"""
            SEO Analyzer Report
            URL: {url}

            Found on Site:
            {found}

            Not Found on Site:
            {not_found}
          """)

seo_analyzer("https://pythonology.eu/what-is-syntax-in-programming-and-linguistics/")
