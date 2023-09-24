from bs4 import BeautifulSoup
import requests
import smtplib

url = "https://books.toscrape.com/catalogue/sapiens-a-brief-history-of-humankind_996/index.html"

contents = requests.get(url).content

soup = BeautifulSoup(contents, 'html.parser')
title = soup.find('img').attrs['alt']
price = float(soup.find('p', class_ = 'price_color').text[1:])

if price < 60:
    # Creating connection to gmail domain via TLS port 587
    connection = smtplib.SMTP('smtp.gmail.com', 587)
    connection.ehlo() # greeting gmail domain
    connection.starttls() # starting TLS security

    # providing log-in
    connection.login('imatesin6@gmail.com', 'cwlhyvaoyjyhntcc')

    # sending email
    connection.sendmail('imatesin6@gmail.com', # from who?
                        'roseyaidata@gmail.com', # to who?
                        f'Subject: Price Drop Notifier\n\n'
                        f'Hello Nellie! \n\nThe price for {title} has dropped to {price}.\n\n'
                        f'Time to buy it :D!') # Say what?
    
    # Closing connection
    connection.quit()