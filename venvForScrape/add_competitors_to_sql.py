import pandas as pd
import sqlite3

# Step 1: Read the CSV file into a DataFrame
#csv_file_path = '/home/titan/Desktop/Bussiness/SoftwareTools/LeadGeneration/EmailExtractor/venvForScrape/input/test2 - compatitors_table2.csv'  # Replace with your CSV file path


df = pd.read_csv(csv_file_path)

# Step 2: Create or connect to an SQLite database
def add_df_to_sql(df):
    conn = sqlite3.connect('website_leads.db')
    cur = conn.cursor()
    # Step 3: Create a table in the SQLite database from the DataFrame
    table_name = 'competitors_raw_table'  # Replace with your desired table name
    df.to_sql(table_name, conn, if_exists='replace', index=False)

    
def added_status_m():
    conn = sqlite3.connect('website_leads.db')
    cursor = conn.cursor()

    # SQL query to update the values in the added_status_m column to 1
    update_query = "UPDATE competitors_raw_table SET added_status_m = 1"
    try:
        cursor.execute(update_query)
        conn.commit()  # Commit the changes
        print("All values in 'added_status_m' set to 1.")
    except Exception as e:
        print(f"An error occurred: {e}")

    # Close the database connection
    conn.close()
def add_csv_to_sqlite(csv_file_path, db_file_path='website_leads.db'):
    """
    Adds data from a CSV file to an SQLite table, setting added_status_m to 0 for all rows.

    :param csv_file_path: Path to the CSV file
    :param db_file_path: Path to the SQLite database file
    """
    # Step 1: Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file_path)

    # Step 2: Add the 'added_status_m' column with default value 0
    df['added_status_m'] = 0

    # Step 3: Connect to the SQLite database
    conn = sqlite3.connect(db_file_path)

    # Step 4: Insert the DataFrame into the SQLite table
    table_name = 'competitors_raw_table'
    df.to_sql(table_name, conn, if_exists='append', index=False)

    # Close the database connection
    conn.close()
    print(f"Data from {csv_file_path} added to {table_name} in SQLite database.")

#add_df_to_sql(df)
# added_status_m()
csv_file = "/home/titan/Desktop/Python/ForMarketing/google-maps-scraper/output/test-5/csv/places-of-test-5.csv"
add_csv_to_sqlite(csv_file)