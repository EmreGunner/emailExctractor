import re
import time
import sqlite3
from bs4 import BeautifulSoup
from scrapy.crawler import CrawlerProcess
from scrapy.http import HtmlResponse
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from read_urls_from_db import read_unchecked_websites,read_checked_websites

check_subpages = False

class MySpider(CrawlSpider):
    name = 'MySpider'
    allowed_domains = [] # Fill this with your allowed domains
    start_urls = read_unchecked_websites()

    rules = (
        Rule(LinkExtractor(allow=(), deny=('mailto:', 'javascript:', 'tel:')), callback='parse_item', follow=True),
    )

def parse_item(self, response):
    print(f"Extracting emails from {response.url}")
    mails = extract_mails(response.text)
    save_emails_to_db(response.url, mails)
    if check_subpages:
        href_links = get_href_links(response.text)
        for href in href_links:
            if href.startswith('/'):
                href = response.urljoin(href)
            self.crawler.engine.crawl(self.request(href, callback=self.parse_item), self)
            
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
    if (email.endswith('.jpg') or email.endswith('.png')):
        return False
    return True

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

process = CrawlerProcess()
process.crawl(MySpider)
process.start()