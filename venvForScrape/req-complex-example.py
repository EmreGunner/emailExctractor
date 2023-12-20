import re
import requests
from urllib.parse import urlsplit
from collections import deque
from bs4 import BeautifulSoup
import pandas as pd

# read url from input
original_url = input("Enter the website url: ") 
 
# to save urls to be scraped
unscraped = deque([original_url])
 
# to save scraped urls
scraped = set()
 
# to save fetched emails
emails = set()  

while len(unscraped):
    # move unsraped_url to scraped_urls set
    url = unscraped.popleft()  # popleft(): Remove and return an element from the left side of the deque
    print("Checking the website : ",url)
    scraped.add(url)
    
    parts = urlsplit(url)
    print("Splitting the url ",parts)
    base_url = "{0.scheme}://{0.netloc}".format(parts)
    print("Base  url ",base_url)
    if '/' in parts.path:
        path = url[:url.rfind('/')+1]
    else:
        path = url
    try:
        response = requests.get(url)
    except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
        # ignore pages with errors and continue with next url
        continue
    # You may edit the regular expression as per your requirement
    new_emails = set(re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.com", 
                  response.text, re.I)) # re.I: (ignore case)
    emails.update(new_emails)
     # create a beutiful soup for the html document
    soup = BeautifulSoup(response.text, 'lxml')
    for anchor in soup.find_all("a"): 
        
        # extract linked url from the anchor
        if "href" in anchor.attrs:
          link = anchor.attrs["href"]
        else:
          link = ''
        
        # resolve relative links (starting with /)
        if link.startswith('/'):
            link = base_url + link
            
        elif not link.startswith('http'):
            link = path + link
        
        if not link.endswith(".gz" ):
          if not link in unscraped and not link in scraped:
              unscraped.append(link)