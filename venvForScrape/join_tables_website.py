import sqlite3

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('website_leads.db')  # Replace with your database file path
cursor = conn.cursor()

def add_merged_data_from_gmaps():
    # Connect to the SQLite database
    conn = sqlite3.connect('website_leads.db')  # Replace with your database file path
    cursor = conn.cursor()

    # Insert data into merged_result from gmaps_lawyers_all
    cursor.execute("""
        INSERT INTO merged_result (place_id, name, main_category, rating, reviews, website, phone, address, link, is_spending_on_ads, email)
        SELECT 
            g.place_id,
            g.name,
            g.main_category,
            g.rating,
            g.reviews,
            g.website,
            g.phone,
            g.address,
            g.link,
            g.is_spending_on_ads,
            e.email
        FROM 
            gmaps_lawyers_all g
        LEFT JOIN 
            emails e ON g.website = e.website
        WHERE
            e.website IS NOT NULL;
    """)
    print("Data from gmaps_lawyers_all inserted into 'merged_result'.")

    # Commit changes and close the connection
    conn.commit()
    conn.close()

# Check if the merged_result table exists
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='merged_result';")
table_exists = cursor.fetchone()

# If the table does not exist, create it
if not table_exists:
    create_table_query = """
    CREATE TABLE merged_result AS
    SELECT 
        c.*,
        e.email
    FROM 
        competitors_raw_table c
    LEFT JOIN 
        emails e ON c.website = e.website;
    """
    cursor.execute(create_table_query)
    print("Table 'merged_result' created and data inserted.")
else:
    print("Table 'merged_result' already exists.")

# Commit changes and close the connection
conn.commit()
conn.close()
add_merged_data_from_gmaps()