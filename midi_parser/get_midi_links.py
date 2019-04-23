#This script uses the beautifulsoup package to scrape the html docs
#Download the files with cat midi_links | xargs wget


from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse

html_doc = open("midi_site.html")
soup = BeautifulSoup(html_doc, "html.parser")

f = open("midi_links","w+")
# Set data path
for link in soup.select("a[href*=mid]"):
    f.write(link.get('href') + " ")
    #url = link.get('href')
    #file = requests.get(url)
    #open("path").write(file.content)
