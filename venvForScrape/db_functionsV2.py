import sqlite3
import time
import logging

#logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
logging.basicConfig(filename='app.log', filemode='w', format='%(asctime)s - %(message)s', level=logging.INFO)

def read_unchecked_websites():
    conn = sqlite3.connect('website_leads.db')
    cur = conn.cursor()
    cur.execute('SELECT website FROM gmaps_lawyers_all')
    rows = cur.fetchall()
    urls = [row[0] for row in rows]
    conn.close()   
    return urls
    # Add the scheme to the URLs

def read_checked_websites():
    conn = sqlite3.connect('website_leads.db')
    cur = conn.cursor()
    cur.execute('SELECT website FROM gmaps_lawyers_all')
    rows = cur.fetchall()
    urls = [row[0] for row in rows]
    conn.close()   
    return urls
    # Add the scheme to the URLs
 
def save_emails_to_db(website, emails,domain = "",error = ""):
    # Connect to the SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect('website_leads.db')
    # Create a cursor object to execute SQL commands
    cur = conn.cursor()
    # Create the 'emails' table if it doesn't exist
    cur.execute('''CREATE TABLE IF NOT EXISTS emails (website TEXT, email TEXT, last_scanned TEXT, domain TEXT, error TEXT)''')
    # Insert the emails into the SQLite database
    if(type(emails) is list):
        if len(emails)>1:
            for email in emails:
                cur.execute('''INSERT INTO emails (website, email, last_scanned,domain,error) VALUES (?, ?, ?, ?, ?)''', (website, email, time.strftime("%Y-%m-%d %H:%M:%S"),domain,error))
        elif len(emails)==1:
            cur.execute('''INSERT INTO emails (website, email, last_scanned,domain,error) VALUES (?, ?, ?, ?, ?)''', (website, emails[0], time.strftime("%Y-%m-%d %H:%M:%S"),domain,error))
        elif(emails):
            try:
                cur.execute('''INSERT INTO emails (website, email, last_scanned,domain,error) VALUES (?, ?, ?, ?, ?)''', (website, emails, time.strftime("%Y-%m-%d %H:%M:%S"),domain,error))
            except IndexError:
                cur.execute('''INSERT INTO emails (website, email, last_scanned,domain,error) VALUES (?, ?, ?, ?, ?)''', (website,"", time.strftime("%Y-%m-%d %H:%M:%S"),domain,"email index error"))    
        else:
            text = type(emails)
            print(text)
            cur.execute('''INSERT INTO emails (website, email, last_scanned,domain,error) VALUES (?, ?, ?, ?, ?)''', (website, "", time.strftime("%Y-%m-%d %H:%M:%S"),domain,"error with mail variable"))
    elif type(emails) is str:
        print("email type is str")
        cur.execute('''INSERT INTO emails (website, email, last_scanned,domain,error) VALUES (?, ?, ?, ?, ?)''', (website, "", time.strftime("%Y-%m-%d %H:%M:%S"),domain,"error with mail variable"))
    else:
        print("this is the case ")
        print(type(emails))
        cur.execute('''INSERT INTO emails (website, email, last_scanned,domain,error) VALUES (?, ?, ?, ?, ?)''', (website, "", time.strftime("%Y-%m-%d %H:%M:%S"),domain,"error with mail variable"))
    conn.commit()
    conn.close()
    print("---------------SAVED----------------------------")
    print(website, emails, time.strftime("%Y-%m-%d %H:%M:%S"))

def save_errored_website(website, emails,domain="",error=""):
    # Connect to the SQLite database (or create it if it doesn't exist)
    logging.error('%s raised an error',website)
    conn = sqlite3.connect('website_leads.db')

    # Create a cursor object to execute SQL commands
    cur = conn.cursor()
    # Create the 'emails' table if it doesn't exist
    cur.execute('''CREATE TABLE IF NOT EXISTS emails (website TEXT, email TEXT, last_scanned TEXT, domain TEXT, error TEXT)''')
    # Insert the emails into the SQLite database

    try:
        cur.execute('''INSERT INTO emails (website, email, last_scanned,domain,error) VALUES (?, ?, ?, ?, ?)''', (website, emails, time.strftime("%Y-%m-%d %H:%M:%S"),domain,error))
    except:
        cur.execute('''INSERT INTO emails (website, email, last_scanned,domain,error) VALUES (?, ?, ?, ?, ?)''', (website,"", time.strftime("%Y-%m-%d %H:%M:%S"),domain,error))    
    
    conn.commit()
    conn.close()

def check_url_exist_db(website):
    # Connect to the SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect('website_leads.db')
    # Create a cursor object to execute SQL commands
    cur = conn.cursor()
    cur.execute('SELECT website FROM emails')
    rows = cur.fetchall()
    urls = [row[0] for row in rows]
    conn.close()   
    if website in urls:
        return True
    else:
        return False

def check_difference():
    # Connect to the SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect('website_leads.db')
    # Create a cursor object to execute SQL commands
    cur = conn.cursor()
    cur.execute("""SELECT website FROM gmaps_lawyers_all WHERE website NOT IN  (SELECT website FROM emails)""")
    rows = cur.fetchall()
    urls = [row[0] for row in rows]
    conn.close()   
    return urls
def test_func():
     # Connect to the SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect('website_leads.db')
    # Create a cursor object to execute SQL commands
    cur = conn.cursor()
    cur.execute('''INSERT INTO emails (website, email, last_scanned) VALUES (?, ?, ?)''', ("https://shop-camouflage.com/", "test", time.strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

def emails_per_domain():
    # Connect to the SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect('website_leads.db')
    # Create a cursor object to execute SQL commands
    cur = conn.cursor()

    # Query to get the count of emails per domain
    cur.execute("""SELECT SUBSTR(email, INSTR(email, '@') + 1) AS domain, COUNT(*) AS email_count 
                   FROM emails 
                   GROUP BY domain""")

    # Fetch all rows and store the results in a dictionary
    rows = cur.fetchall()
    domain_counts = {row[0]: row[1] for row in rows}

    conn.close()   
    return domain_counts

def check_value(val,col,table):
      # Connect to the SQLite database
    conn = sqlite3.connect('website_leads.db')
    # Create a cursor object
    cur = conn.cursor()
        # Prepare the SQL query. Parameters are passed using ? to prevent SQL injection
    query = f"SELECT EXISTS(SELECT 1 FROM {table} WHERE {col} = ? LIMIT 1)"

    # Execute the query with the provided value
    cur.execute(query, (val,))
    
    # Fetch the result
    result = cur.fetchone()[0]
    
    # Close the database connection
    conn.close()
    
    # Return True if the value exists, False otherwise
    return bool(result)
    
def update_status_in_db(website, new_status):
    # Connect to the SQLite database
    with sqlite3.connect('website_leads.db') as conn:
        # Create a cursor object
        cur = conn.cursor()
        try:
            # Prepare and execute the update query
            cur.execute("UPDATE emails SET status = ? WHERE website = ?", (new_status, website))
            conn.commit()
        except sqlite3.Error as e:
            print(f"An error occurred while updating status: {e}")

def get_status():
    # SQL query to count websites with status = 1
    total_query = "SELECT COUNT(*) FROM emails"
    total = sql_executer(total_query)    
    no_email_query = "SELECT COUNT(*) FROM emails WHERE email = '' OR email IS NULL"
    no_email = sql_executer(no_email_query)    
    status_on_query = "SELECT COUNT(*) FROM emails WHERE status = 1"
    status_on = sql_executer(status_on_query)
    status_off_query = "SELECT COUNT(*) FROM emails WHERE status <> 1 OR status IS NULL AND email <> '' AND email IS NOT NULL"
    status_off = sql_executer(status_off_query)
    total_with_mail_query =  "SELECT COUNT(*) FROM emails WHERE email <> '' AND email IS NOT NULL"
    total_with_mail = sql_executer(total_with_mail_query)
    status_obj = {'total':total,
                  'No Email':no_email,
                  'Total With Mail':total_with_mail,
                  "Sent Website":status_on,
                  "Not sent mail ":status_off}
    return status_obj
    # Execute the query

def sql_executer(query):
    # Connect to the SQLite database
    conn = sqlite3.connect('website_leads.db')
    cur = conn.cursor()
    try:
        cur.execute(query)
        count = cur.fetchone()[0]
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        count = None
    finally:
        # Close the database connection
        conn.close()
    return count

status = get_status()
print(status)
#test_func()
#difference = check_difference()
#stat_mail = emails_per_domain()
#print(stat_mail)
#res_check = check_value(val="http://www.kivamhukuk.com/",col="website",table="emails")