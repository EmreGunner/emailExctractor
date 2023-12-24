from db_functionsV2 import *
import re
import time
from urllib.parse import urlsplit
import logging
import requests
import extractor
from bs4 import BeautifulSoup

#-----------VARIABLE ASSIGNMENTS-------------
#current time
start_time = time.time()

#get unchecked urls from db
unchecked_websites = read_unchecked_from_merged()

#list of checked websites
checked_websites = []

#print("unchecked websites ",unchecked_websites)

#-----------CONFIGS---------------------------
get_subpages = True

#logging
logging.basicConfig(filename='main.log', encoding='utf-8', level=logging.DEBUG)
logging.info("started")

#----------MAIN SCRIPT-------------------

#Comment to myself:
#Add seperate table for the urls with problems | Columns | Site | emails | lastscan | error
def check_url_schema(url):
    if url.startswith('http://') or url.startswith('https://'):
            return True
    else:
        return False

def get_domain(url):
    full_url = url
    url_parts = urlsplit(full_url)
    return url_parts.netloc
    
        
#Comment to myself:
#Add seperate table for the urls with problems | Columns | Site | emails | lastscan | error
def fix_urls(urls):
    # Add the scheme to the URLs
    urls_with_scheme = []
    print("URLS ",urls)
    for url in urls:
        if(url):
            if (check_url_schema(url)):
                urls_with_scheme.append(url)
            else:
                urls_with_scheme.append('http://' + url)
        else:
            logging.error("No URL found! for : ",url)
    return urls_with_scheme    

def get_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    try:
        logging.info('%s requesting page : ',url)
        response =  requests.get(url,headers=headers,timeout=6)
        if response.status_code == 200:
            content = response.text
            return content
        else:
            logging.error('Error %d while getting page from %s',response.status_code,url)
            return None
    except:
        print("Failed to load the webpage:", url)
        #error should go to db
        return None
def get_href_links(html):
    logging.info("getting sub pages")
    soup = BeautifulSoup(html, 'html.parser')
    word_list = ['iletisim', 'contact']
    href_links = [a['href'] for a in soup.find_all('a', href=True) if any(word in a['href'] for word in word_list)]
    return href_links

def process_href(href, main_url):
    """
    Process the href link, extract emails, and save them to the database.
    """
    # Check if the href has a valid URL schema or is a relative path
    url = main_url
    if not check_url_schema(href):
        if href.startswith('/'):
            base_url = f'{urlsplit(url).scheme}://{urlsplit(url).netloc}'
            href = base_url + href
        else:
            logging.info("%s BAD LINK CHECK SUBPAGE", href)
            return
     # Log and skip processing if the href is already checked or exists in the database
    if href in checked_websites or href == url:
        logging.info("%s SKIPPING URL, IT ALREADY EXISTS ", href)
        return
    logging.info("%s CHECKING SUBPAGE", href)
    checked_websites.append(href)  # Add href to the list of checked websites
    try:
        page_content = get_page(href)
        if page_content:
            mails = extractor.extract_mails(page_content)
            print(f"Extracted Emails {mails} from sub page: {href}")
            logging.info(f"Extracted Emails {mails} from sub page: {href}")
            save_emails_to_merged_result(website=href, emails=mails,domain= get_domain(href),is_sub_page=True,main_website_url=main_url)  
        else:
            logging.info(f"Error with subpage {href}")
            save_errored_website(href, error="could n   ot reach site",main_url=main_url)
    except Exception as e:
        print(f"Error while processing link: {href}")
        logging.error(f"Error message: {e}")
    
urls = fix_urls(unchecked_websites[10:21])
print(urls)
url_count = len(urls)

for url in urls:
    logging.info("%s URL COUNT ",url_count)
    url_count = (url_count  - 1)
    if(url not in checked_websites):
        print("%s URL COUNT ",url_count) 
        checked_websites.append(url)       
        domain = get_domain(url)
        logging.info("%s CHECKING ",url)
        #skipped checking db
        #if(check_url_exist_db(url)):
            #logging.info("%s SKIPPING URL, IT ALREADY EXISTS IN DB",url)
            #print("%s SKIPPING URL, IT ALREADY EXISTS IN DB",url)
            #continue
        if "instagram.com" in url:
            continue
        logging.info("%s URL NOT EXISTS ",url)
        html = get_page(url)
        if(html):
            print(f"extracting emails from website {url}")
            mails = extractor.extract_mails(html)
            print("Extracted Emails from home page: ", mails)
            logging.info("%s EXTRACTED MAILS ",mails)
            save_emails_to_merged_result(url,mails,domain)
            if(get_subpages):
                    href_links = get_href_links(html)
                    href_links = list(set(href_links))
                    logging.info("%s GOT HREF LINKS", ', '.join(href_links))
                    for href in href_links:
                        process_href(href=href,main_url=url)
        else:
            print(f"there was a error with {url}")
            logging.info(f"there was a error with {url}")
            save_errored_website(url,domain=domain,error="could not reach site")
    else:
        print("%s SKIPPING URL, IT ALREADY EXISTS IN CACHE (LIST) ",url)
        logging.info("%s SKIPPING URL, IT ALREADY EXISTS IN CACHE ",url)
        continue
    
#type of check
#Competitor Loop