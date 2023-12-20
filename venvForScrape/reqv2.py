from db_functions import read_unchecked_websites,save_emails_to_db,check_url_exist_db,save_errored_website
from bs4 import BeautifulSoup
import requests
import re
import time
from urllib.parse import urlsplit
import logging

logging.basicConfig(filename='app.log', encoding='utf-8', level=logging.DEBUG)
start_time = time.time()
logging.info("started")
unchecked_websites = read_unchecked_websites()
check_subpages = True


#Comment to myself:
#Add seperate table for the urls with problems | Columns | Site | emails | lastscan | error
def fix_urls(urls):
    # Add the scheme to the URLs
    urls_with_scheme = []
    for url in urls:
        if url.startswith('http://') or url.startswith('https://'):
            urls_with_scheme.append(url)
        else:
            urls_with_scheme.append('http://' + url)
    return urls_with_scheme


def get_page(url):
    try:
        logging.info('%s got the page ',url)
        response =  requests.get(url,timeout=6)
        content = response.text
        #print(" ----CONTENT ----" ,content)
        #print("Content URL : -- ",content)
        return content
    except:
        print("Failed to load the webpage:", url)
        return None
    
def get_href_links(html):
    logging.info("getting sub pages")
    soup = BeautifulSoup(html, 'html.parser')
    word_list = ['contact', 'customer', 'privacy', 'terms', 'refund']
    href_links = [a['href'] for a in soup.find_all('a', href=True) if any(word in a['href'] for word in word_list)]
    return href_links

def extract_mails(html):
    pattern = r"[a-zA-Z0-9\.\-+_]+@[a-zA-Z0-9\.\-+_]+\.[a-z]+"
    #logging.info('%s got the content ',html)
    all_mails = re.findall(pattern, html)
    mails = []
    if not all_mails:
        print("No email found.")
        return "no-email-found"
    else:
        if(type(all_mails) is list):
            print("got mails as list")
            for mail in all_mails:
                print("MAIL :" ,mail)
                if mail not in mails: 
                    if(validate_email(mail)):
                        mails.append(mail)
        if(type(all_mails) is str):
            print("got mails as STR")
            print("MAIL :" ,mail)
            if mail not in mails: 
                    if(validate_email(mail)):
                        mails.append(mail)
        return list(set(mails))
 
def validate_email(email):
    if not re.match(r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$', email):
        return False
    if email[0].isdigit():
        return False
    if  (email.endswith('.jpg') or email.endswith('.png') or email.endswith('.webp')):
        return False
    return True

urls = fix_urls(unchecked_websites)
#print(urls)

for url in urls:
    print("Got the url:  ", url)
    if(check_url_exist_db(url)):
        print(f"skipping  {url} it already exists")
        continue
    print("--- %s seconds ---" % (time.time() - start_time))
    html = get_page(url)
    if html:
        print(f"extracting emails from website {url}")
        mails = extract_mails(html)
        print("Extracted Emails from home page: ", mails)
        save_emails_to_db(url,mails)
        if (check_subpages):
            href_links = get_href_links(html)  
            for href in href_links:
                try:
                    if(href==url):
                        logging.info("print href url exist 1")
                        continue
                    logging.info("%s got the sub pages",href)
                    print("---------------FOR WEBSITE ----------------",url)
                    print("---------------HREF LINKS ----------------",href)
                    if(href.startswith('http') or  href.startswith('https')):
                        if(check_url_exist_db(href)):
                            print(f"skipping  {href} it already exists")
                            continue
                        print(f"checking page {href}")
                        mails = extract_mails(get_page(href))
                        print("Extracted Emails: ", mails)
                        save_emails_to_db(href, mails)
                    elif(href.startswith('/')):
                        full_url = url
                        url_parts = urlsplit(full_url)
                        base_url = url_parts.scheme + "://" + url_parts.netloc
                        href = base_url + href
                        if(href==url):
                            logging.info("print href url exist 2")
                            continue
                        if(check_url_exist_db(href)):
                            print(f"skipping  {href} it already exists")
                            continue
                        if "mailto" in href:
                            save_emails_to_db(url, href)    
                            continue
                        print(f"checking page {href}")
                        
                        mails = extract_mails(get_page(href))
                        print("Extracted Emails: ", mails)
                        save_emails_to_db(href, mails)
                except Exception as e:
                    print("Error while processing link: ", href)
                    print("Error message: ", str(e))
        else:
            print("Skipping subpages")
                        
    else:
        print(f"there was a error with {url}")
        save_errored_website(url,"could not reach site")




