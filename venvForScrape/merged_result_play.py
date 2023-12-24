import sqlite3
import pandas as pd
from urllib.parse import urlsplit

DB_PATH = 'website_leads.db'  # Define your database file path here

def execute_sql(query, params=None, fetch=False):
    """
    Execute an SQL query on the SQLite database.

    :param query: SQL query to execute.
    :param params: Parameters for the SQL query.
    :param fetch: Boolean indicating if the results should be fetched.
    :return: Fetched data if fetch is True, otherwise None.
    """
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(query, params or ())
        if fetch:
            return cursor.fetchall()
        conn.commit()
def get_domain(url):
    if url:
        url_parts = urlsplit(url)
        domain = url_parts.netloc
        if domain.startswith('www.'):
            domain = domain.replace('www.', '', 1)
        return domain
    else:
        return None
    
def get_status_db():
    total_records = execute_sql("SELECT COUNT(*) FROM merged_result;", fetch=True)[0][0]
    records_with_website = execute_sql("SELECT COUNT(*) FROM merged_result WHERE website IS NOT NULL AND website != '';", fetch=True)[0][0]
    records_with_email = execute_sql("SELECT COUNT(*) FROM merged_result WHERE website IS NOT NULL AND website != '' AND email IS NOT NULL AND email != '';", fetch=True)[0][0]
    
    print(f"Total records: {total_records}")
    print(f"Records with website: {records_with_website}")
    print(f"Records where website has email: {records_with_email}")
def get_status_df(df):
    total_records = len(df)
    records_with_website = df['website'].apply(lambda x: x is not None and x != '').sum()
    records_with_email = df[(df['website'].apply(lambda x: x is not None and x != '')) & 
                            (df['email'].apply(lambda x: x is not None and x != ''))].shape[0]

    print(f"Total records (filtered): {total_records}")
    print(f"Records with website (filtered): {records_with_website}")
    print(f"Records where website has email (filtered): {records_with_email}")

def delete_duplicate_places():
    delete_query = """
    DELETE FROM merged_result
    WHERE rowid NOT IN (
        SELECT MIN(rowid)
        FROM merged_result
        GROUP BY place_id, email
    );
    """
    rows_affected = execute_sql(delete_query)
    print(f"Deleted duplicates from merged_result. Rows affected: {rows_affected}")

def filter_by_main_category(categories):
    placeholders = ','.join('?' for _ in categories)
    query = f"SELECT * FROM merged_result WHERE main_category IN ({placeholders})"
    df = pd.read_sql_query(query, sqlite3.connect(DB_PATH), params=categories)
    return df
def get_email_domain(email):
    if pd.isna(email) or "@" not in email:
        return None
    return email.split('@')[1].lower()
def add_columns(df):
    # Add domain column
    df['domain'] = df['website'].apply(get_domain)
    # Add other columns as needed in the future
    # Add email_domain column
    df['email_domain'] = df['email'].apply(get_email_domain)
    # Add email_domain_match column
    df['email_domain_match'] = df.apply(
        lambda row: (row['domain'] == row['email_domain']) if pd.notna(row['domain']) and pd.notna(row['email_domain']) else None, 
        axis=1
    )
    return df

if __name__ == "__main__":
    get_status_db()
    #delete_duplicate_places()
    # Call the function and print the resulting DataFrame
 # Define the main categories
    categories = [
    'Hukuk Burosu',
    'Avukat',
    'Hukuk Hizmetleri',
    'Avukatlik Danisma Hizmeti',
    'Bosanma Avukati',
    'Ceza Avukati',
    'Patent Avukati',
    'Hukuki Isler Burosu',
    'Is Hukuku Avukati',
    'Dava Avukati',
    'Avukatlar Dernegi',
    'Gocmenlik Hukuku Avukati',
    'Gayrimenkul Hukuku Avukati',
    'Aile Hukuku Avukati']
    df_filtered = filter_by_main_category(categories)
    print(df_filtered)
    df_filtered = add_columns(df_filtered)
    get_status_df(df_filtered)