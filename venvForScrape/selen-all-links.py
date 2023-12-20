from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
import re
import sqlite3
import time 
from bs4 import BeautifulSoup
from read_urls_from_db import read_unchecked_websites,read_checked_websites
#Variables definitions
#Configs
check_subpages = False

websites = read_unchecked_websites()
#selenium-variables

service = Service(executable_path="/snap/bin/geckodriver")
options = webdriver.FirefoxOptions()
driver = webdriver.Firefox(service=service, options=options)

def get_page(website):
    try:
        driver.get(website)
        html = driver.page_source
        return html
    except WebDriverException as e:
        print("Failed to load the webpage:", website)
        print("Error message:", str(e))
        return None

def get_href_links(html):
    soup = BeautifulSoup(html, 'html.parser')
    word_list = ['contact', 'customer', 'privacy', 'terms', 'refund']
    href_links = [a['href'] for a in soup.find_all('a', href=True) if any(word in a['href'] for word in word_list)]
    return href_links

def extract_mails(html):
    pattern = r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+"
    all_mails = re.findall(pattern, html)
    mails = []
    if not all_mails:
        print("No email found.")
        return "no-email-found"
    else:
        if(type(all_mails) is list):
            for mail in all_mails:
                print("MAIL :" ,mail)
                if mail not in mails: 
                    if(validate_email(mail)):
                        mails.append(mail)
        if(type(all_mails) is str):
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
    if  (email.endswith('.jpg') or email.endswith('.png')):
        return False
    return True

def website_url_checker(website): 
    base = "http://"
    if not website.startswith('http') or not website.startswith('https'):
        link = base + website
        return link
    else:
        return website

def save_emails_to_db(website, emails):
    # Connect to the SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect('website_leads.db')

    # Create a cursor object to execute SQL commands
    cur = conn.cursor()
    # Create the 'emails' table if it doesn't exist
    cur.execute('''CREATE TABLE IF NOT EXISTS emails
                   (website TEXT, email TEXT, last_scanned TEXT)''')
    # Insert the emails into the SQLite database
    if(type(emails) is list):
        for email in emails:
            cur.execute('''INSERT INTO emails (website, email, last_scanned) VALUES (?, ?, ?)''', (website, email, time.strftime("%Y-%m-%d %H:%M:%S")))
    if(type(emails) is str):
        cur.execute('''INSERT INTO emails (website, email, last_scanned) VALUES (?, ?, ?)''', (website, emails, time.strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

print(f"GATHERED WEBSITES {websites}")    
for website in websites:
    website = website_url_checker(website)
    print(f"checking website {website}")
    checked_websites =  read_checked_websites()
    if website not in checked_websites:
        html = get_page(website)
        if html:
            print(f"extracting emails from website {website}")
            mails = extract_mails(html)
            print("Extracted Emails from home page: ", mails)
            save_emails_to_db(website,mails)
            if (check_subpages):
                href_links = get_href_links(html)    
                for href in href_links:
                    try:
                        print("---------------HREF LINKS----------------",href)
                        if(href.startswith('/')):
                            href = website + href
                        if "mailto" in href:
                            save_emails_to_db(href, href)    
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
            pass
    else:
        print(f"website already checked {website}")
    
    time.sleep(1)
