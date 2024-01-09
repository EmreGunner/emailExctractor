import sqlite3
import time
import logging

#logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
logging.basicConfig(filename='app.log', filemode='w', format='%(asctime)s - %(message)s', level=logging.INFO)

def read_unchecked_websites():
    conn = sqlite3.connect('website_leads.db')
    cur = conn.cursor()
    cur.execute('SELECT website FROM competitors_raw_table WHERE website IS NOT NULL AND added_status_m <> 1')
    rows = cur.fetchall()
    urls = [row[0] for row in rows]
    conn.close()   
    return urls
    # Add the scheme to the URLs

def read_unchecked_from_merged():
    conn = sqlite3.connect('website_leads.db')
    cur = conn.cursor()
    cur.execute('SELECT website FROM merged_result WHERE website IS NOT NULL AND email IS NULL OR email IS "could not reach site" OR email is "" AND recheck_status = 0 ')
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

def save_emails_to_merged_result(website, emails, domain="", error="", is_sub_page=False, main_website_url=None):
    conn = None
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect('website_leads.db')
        cur = conn.cursor()
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")

        if is_sub_page and main_website_url:
            # Retrieve data from the main website's row
            cur.execute('SELECT * FROM merged_result WHERE website = ?', (main_website_url,))
            main_website_data = cur.fetchone()

            if main_website_data:
                # Create a new row with the existing data except for website, emails, domain, and error
                cur.execute('''
                    INSERT INTO merged_result (place_id, name, main_category, rating, reviews, website, phone, 
                                               address, link, is_spending_on_ads, email, last_scanned, domain, error)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    main_website_data[0], main_website_data[1], main_website_data[2], main_website_data[3],
                    main_website_data[4], website, main_website_data[6], main_website_data[7],
                    main_website_data[8], main_website_data[9], ', '.join(emails) if isinstance(emails, list) else emails,
                    current_time, domain, error
                ))
        else:
            email_str = ', '.join(emails) if isinstance(emails, list) else emails
            # Check if website already exists
            cur.execute('SELECT COUNT(*) FROM merged_result WHERE website = ?', (website,))
            if cur.fetchone()[0] > 0:
                # Update existing record
                cur.execute('''
                    UPDATE merged_result 
                    SET email = ?, domain = ?, error = ?, last_scanned = ?
                    WHERE website = ?
                ''', (email_str, domain, error, current_time, website))
            else:
                # Insert new record
                cur.execute('''
                    INSERT INTO merged_result (website, email, domain, error, last_scanned)
                    VALUES (?, ?, ?, ?, ?)
                ''', (website, email_str, domain, error, current_time))
          # After inserting or updating the record, update recheck_status
        cur.execute('UPDATE merged_result SET recheck_status = 1 WHERE website = ?', (website,))
        conn.commit()
        logging.info(f"Data successfully updated for website: {website}")

    except sqlite3.Error as e:
        logging.error(f"SQLite error in save_emails_to_merged_result: {e}")
    finally:
        if conn:
            conn.close()

# Example usage
#logging.basicConfig(filename='app.log', level=logging.INFO)
#save_emails_to_merged_result('example.com', ['email@example.com'], 'example.com', 'No error')
def save_errored_website(website, domain, error):
    conn = None
    try:
        conn = sqlite3.connect('website_leads.db')
        cur = conn.cursor()
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")

        # Check if website already exists in the database
        cur.execute('SELECT COUNT(*) FROM merged_result WHERE website = ?', (website,))
        if cur.fetchone()[0] > 0:
            # Update existing record
            cur.execute('''
                UPDATE merged_result 
                SET domain = ?, error = ?, last_scanned = ?
                WHERE website = ?
            ''', (domain, error, current_time, website))
        else:
            # Insert new record
            cur.execute('''
                INSERT INTO merged_result (website, domain, error, last_scanned)
                VALUES (?, ?, ?, ?)
            ''', (website, domain, error, current_time))
          # After inserting or updating the record, update recheck_status
        cur.execute('UPDATE merged_result SET recheck_status = 1 WHERE website = ?', (website,))
    
        conn.commit()
        logging.info(f"Error data successfully saved for website: {website}")

    except sqlite3.Error as e:
        logging.error(f"SQLite error in save_errored_website: {e}")
    finally:
        
        if conn:
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
def is_rechecked(website):
    # Connect to the SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect('website_leads.db')
    # Create a cursor object to execute SQL commands
    cur = conn.cursor()
    cur.execute('SELECT recheck_status FROM merged_result WHERE website = ?', (website,))
    result = cur.fetchone()
    conn.close()   
    #print(result)
    if (result[0]==1):
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

def not_send_mails():
    query_not_send_mails = "SELECT * FROM emails WHERE email <> '' AND email IS NOT NULL"
    not_send_mails = sql_executer_fetch_all(query_not_send_mails)
    return not_send_mails
def sql_executer_fetch_all(query):
    # Connect to the SQLite database
    conn = sqlite3.connect('website_leads.db')
    cur = conn.cursor()
    try:
        cur.execute(query)
        ret = cur.fetchall()
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        ret = None
    finally:
        # Close the database connection
        conn.close()
    return ret

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
def add_unique_constraint_to_website():
    conn = None
    try:
        conn = sqlite3.connect('website_leads.db')
        cur = conn.cursor()

        # Add a unique constraint to the 'website' column
        cur.execute('''
            CREATE UNIQUE INDEX IF NOT EXISTS idx_website_unique ON merged_result (website)
        ''')
        conn.commit()
        logging.info("Unique index on 'website' column created successfully.")

    except sqlite3.Error as e:
        logging.error(f"SQLite error in add_unique_constraint_to_website: {e}")
        raise
    finally:
        if conn:
            conn.close()
def reset_recheck_status():
    conn = None
    try:
        conn = sqlite3.connect('website_leads.db')
        cur = conn.cursor()

        # SQL query to update recheck_status to 0 for all rows
        cur.execute('UPDATE merged_result SET recheck_status = 0')
        conn.commit()
        logging.info("Recheck status reset for all records in merged_result.")
    
    except sqlite3.Error as e:
        logging.error(f"SQLite error in reset_recheck_status: {e}")
    finally:
        if conn:
            conn.close()
status = get_status()
print(status)
#test_func()
#difference = check_difference()
#stat_mail = emails_per_domain()
#print(stat_mail)
#res_check = check_value(val="http://www.kivamhukuk.com/",col="website",table="emails")
#print(read_unchecked_websites())
#add_unique_constraint_to_website()
#reset_recheck_status()
#print(is_rechecked("http://www.selverakkoyunkorkmaz.av.tr/"))