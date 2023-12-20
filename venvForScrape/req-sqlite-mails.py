import requests
from bs4 import BeautifulSoup
import re
import sqlite3
from concurrent.futures import ThreadPoolExecutor
import time

    
websites = ["stagshop.com",
"adultfun.ca",
"mchurt.eu",
"stagshop.com",
"regulation.co.uk",
"dildoking.de",
"other-nature.de",
"harmonystore.co.uk",
"venusenvy.ca",
"100shadesofblue.co.uk",
"demonia.com",
"yourperfectmoment.nl",
"prowler.co.uk",
"thealternativeottawa.com",
"orion-store.de",
"wickedwandas.ca",
"pleasuresntreasures.com",
"prowlerred.com",
"sh-womenstore.com",
"gorgeous-berlin.de"
]


start_time = time.time()



def website_url_checker(website): 
    base = "http://"
    if not website.startswith('http') or not website.startswith('https'):
        link = base + website
        return link
    else:
        return website
    
    
def extract_emails(url):
    try:
        print("--- %s seconds ---" % (time.time() - start_time))
        # Send a GET request to the URL
        response = requests.get(url,timeout=10)
        response.raise_for_status() # Raises an HTTPError if the HTTP request returned an unsuccessful status code
    except requests.exceptions.HTTPError as errh:
        print("HTTP Error:",errh)
        return [], str(errh)
    except requests.exceptions.ConnectionError as errc:
        print ("Error Connecting:",errc)
        return [], str(errc)
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error:",errt)
        return [], str(errt)
    except requests.exceptions.RequestException as err:
        print ("Something went wrong:",err)
        return [], str(err)
    soup = BeautifulSoup(response.content, 'html.parser')
    email_elements = soup.find_all(string=re.compile(r'\S+@\S+'))
    #emails = [re.search(r'\b\S+@\S+\b', elem).group() for elem in email_elements]
    # Extract all the emails from the website
    emails = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", soup.text, re.I)
    if emails:
        return emails,"success"
    else:
        return "","extract_failure"


def fetch_and_store_emails(website):
    # Connect to the SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect('website_leads.db')

    # Create a cursor object to execute SQL commands
    cur = conn.cursor()

    website = website_url_checker(website)
    emails,error = extract_emails(website)
    print(("returned emails for website ",emails,website))
    print(("returned errors for website ",error,website))
    

    # If emails were found, store them in the SQLite database
    if len(emails)>0:
        print(f"Emails found on {website} ")
        for email in emails:
            cur.execute('''INSERT INTO emails (website, email, last_scanned, error) VALUES (?, ?, ?, ?)''', (website, email, time.strftime("%Y-%m-%d %H:%M:%S"), error))
        
    elif not emails:
            cur.execute('''INSERT INTO emails (website, email, last_scanned, error) VALUES (?, ?, ?, ?)''', (website, "No-email-found", time.strftime("%Y-%m-%d %H:%M:%S"), error))
            
    else:
        print(f"something went wrong  on {website} ")
    
    conn.commit()
    conn.close()

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('website_leads.db')
cur = conn.cursor()

# Create the table if it doesn't exist
cur.execute('''CREATE TABLE IF NOT EXISTS emails
                 (website TEXT, email TEXT, last_scanned TEXT, error TEXT)''')

conn.commit()
conn.close()

# The following lines of code fetch emails from the specified websites in parallel using ThreadPoolExecutor
executor = ThreadPoolExecutor(max_workers=5)
executor.map(fetch_and_store_emails, websites)
#for website in websites:
    #fetch_and_store_emails(website)

# Commit the changes to the SQLite database and close the connection
print("its coming here as well")




    