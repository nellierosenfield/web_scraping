from nltk.tokenize import word_tokenize
from bs4 import BeautifulSoup
import pandas as pd
import requests
import nltk
import sys
# nltk.download('stopwords')
# nltk.download('punkt')

# For this analyzer, we will be checking for the following:
#     - Are there any warnings?
#     - Is there a title and meta description?
#     - Are there are enough header tags, especially h1?
#     - Do images have atl tags for accessibility?
#     - Do the keywords match or relate to the page title?

def seo_report(url, found, not_found, keywords):
    print(f"""
            SEO Analyzer Report
            URL: {url}

            Found on Site:
            {found}

            Not Found on Site:
            {not_found}

            Most Common Keywords:
            {keywords}
          """)

def most_common_keywords(soup):
    # tokenizing each word in body
    try:
        words = [token.lower() for token in word_tokenize(soup.find('body').text)]

        # collecting list of english stop words for comparison
        stop_words = nltk.corpus.stopwords.words('english')

        # Ensures that only non-stopwords are captured and stored
        words_cleaned = []
        for word in words:
            if word not in stop_words and word.isalpha():
                words_cleaned.append(word)

        # returns the 10 most common words as a list
        return nltk.FreqDist(words_cleaned).most_common(10)
    except:
        return ['No body tag was found! Please correct this!']
    
def url_check(url):
    try:
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Invalid or blocked URL: {url}")
            exit()
        else:
            return response
    except:
        print(f"Invalid or blocked URL: {url}")
        exit()
    
    
def seo_analyzer(url):
    response = url_check(url).text
    soup = BeautifulSoup(response, 'html.parser')

    not_found = [] # What's not found on the site
    found = [] # Items present on the site

    # Is there a title and meta description?
    try:
        title = soup.find('title').text
        if title:
            found.append(f"Title: {title} (size {len(title)})")
        else:
            not_found.append('Title not found! Please add a title to your site')
    except:
        not_found.append('Title tag not found! Please add a title tag to your site')

    try:
        meta_desc = soup.find('meta', attrs = {'name': 'description'})['content']
        if meta_desc:
            found.append(f"Meta Description: {meta_desc}")
        else:
            not_found.append('Meta description not found! Please add a meta description to your site.')
    except:
        not_found.append('Meta description tag not found! Please add a meta description tag to your site.')

    # Are there are enough header tags, especially h1?
    headings = ['h1', 'h2', 'h3']
    heading_tags = []
    try:
        for heading in soup.find_all(headings):
            found.append(f"{heading.name} --> {heading.text.strip()}")
            heading_tags.append(heading.name)

        if 'h1' not in heading_tags:
            not_found.append('No h1 tags found! Please add at least one (1) h1 tag to your site.')
    except:
        not_found.append('No heading tags were found! Please add at least one (1) tag to your site.')

    # Do images have atl tags for accessibility?
    try: 
        for image in soup.find_all('img', alt = ''):
            not_found.append(f"Warning! This image does not contain an alt: {image}")
    except:
        not_found.append("No img tags were found so skipped...")
    
    # Do the keywords match or relate to the page title?
    keywords = most_common_keywords(soup)

    # generates report
    seo_report(url, found, not_found, keywords)

seo_analyzer("https://www.linkedin.com/in/nellierosenfield/")
