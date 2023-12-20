import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('website_leads.db')
cur = conn.cursor()

# Base URL for dummy data
base_url = "http://example.com/page"

# SQL statement for inserting data
sql = "INSERT INTO urls_to_check (website) VALUES (?)"

# Insert 37 rows with different URLs
for i in range(1, 542):  # This will create URLs from page1 to page37
    url = f"{base_url}{i}"
    cur.execute(sql, (url,))

# Commit the changes
conn.commit()

# Close the connection
conn.close()