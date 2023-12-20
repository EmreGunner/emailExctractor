import sqlite3


def read_unchecked_websites():
    conn = sqlite3.connect('website_leads.db')
    cur = conn.cursor()
    cur.execute('SELECT website FROM urls_to_check')
    rows = cur.fetchall()
    urls = [row[0] for row in rows]
    conn.close()   
    return urls
    # Add the scheme to the URLs
    
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


