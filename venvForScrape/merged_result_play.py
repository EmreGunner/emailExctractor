import sqlite3
import pandas as pd
from urllib.parse import urlsplit
import openpyxl
from loca_address_adder import extract,revised_extract
import os

DB_PATH = 'website_leads.db'  # Define your database file path here
# Directory for saving CSV files
output_dir = 'campaign_leads_csvs'
# Create the directory if it does not exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)


sokak_count = cadde_count = mah_count = blv_count = unknown_count = nan_count = plz_count = resi_count = ofc_count= 0
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
       # Add loca column
    #    df['loca'] = df.apply(extract, axis=1)
    
      # Modify this line to apply 'extract' only to the 'loca' column
    df['loca'] = df['address'].apply(extract)  # Assuming 'loca' is a column in df
    df['loca'] = df['loca'].str.strip()
    # Modify this line to apply 'extract' only to the 'loca' column
    df['revised_loca'] = df['address'].apply(extract)  # Assuming 'loca' is a column in df
    df['revised_loca'] = df['revised_loca'].str.strip()

    return df


def filter_by_email_domain(df, excluded_domains, excluded_extensions):
    """
    Filter DataFrame by excluding specified email domains, extensions, and unwanted email values.
    
    :param df: DataFrame to be filtered.
    :param excluded_domains: List of domains to exclude.
    :param excluded_extensions: List of file extensions to exclude.
    :return: Filtered DataFrame.
    """
    # Ensure 'email' column is filled with strings, replacing None or NaN with an empty string
    df['email'] = df['email'].fillna('')

    # Filter out rows where email is "could not reach site", "no-email-found", or empty
    email_filter = ~df['email'].isin(["could not reach site", "no-email-found", ""])

    # Exclude specified domains
    domain_filter = ~df['email_domain'].isin(excluded_domains)

    # Exclude emails ending with specific extensions
    extension_filter = ~df['email'].str.endswith(tuple(excluded_extensions))

    return df[email_filter & domain_filter & extension_filter]
def generate_campaign_sheets(df, daily_sample_size, days):
    """
    Generate campaign sheets for email marketing.

    :param df: DataFrame containing lead data.
    :param sample_size: Total number of samples for each campaign (divided over days).
    :param days: Number of days to distribute the leads.
    :return: Dictionary of DataFrames, each representing a campaign's daily sheet.
    """
    #sample size i changed
    sample_size = daily_sample_size  
    campaign_sheets = {}

    # For each campaign (cA, cB, cC) and each day, create a sample and add to the campaign_sheets
    for campaign in ['cA', 'cB', 'cC']:
        for day in range(1, days + 1):
            # Check if there are enough records left in the DataFrame
            if len(df) < daily_sample_size:
                # If not enough records, take whatever is left
                daily_sample = df
            else:
                # Sample the DataFrame
                daily_sample = df.sample(n=daily_sample_size)
            
            # Remove the selected samples from the DataFrame to avoid repetition
            df = df.drop(daily_sample.index)

            # Name the sheet as per campaign and day
            sheet_name = f"{campaign}_Day{day}"
            campaign_sheets[sheet_name] = daily_sample

    # Return the dictionary containing all the sheets
    return campaign_sheets

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
    # Define the path to the Excel file
    excel_file_path = 'campaign_sheets.xlsx'  # Update this path if needed
    df_filtered = filter_by_main_category(categories)
    
    print(df_filtered)
    df_filtered = add_columns(df_filtered)
    get_status_df(df_filtered)
    # Call the filter function
    excluded_domains = [
    'adresiniz.com', 'godaddy.com', 'example.com', 'yoursite.com', 
    'your-domain.com', 'sirketiniz.com', 'sentry.wixpress.com', 'ornek.com']
    excluded_extensions = ['.jpeg', '.jpg', '.png']
    # Assuming df_filtered is already created from the previous function
    #"could not reach site","no-email-found",""
    df_filtered = filter_by_email_domain(df_filtered, excluded_domains, excluded_extensions)
    print(df_filtered)
    get_status_df(df_filtered)
    # Generate the campaign sheets
    # Use the actual sample size and number of days in your case
    campaign_sheets = generate_campaign_sheets(df_filtered, daily_sample_size=100, days=5)
    #with pd.ExcelWriter('campaign_sheets.xlsx') as writer:
    #    for sheet_name, sheet_data in campaign_sheets.items():
    #        sheet_data.to_excel(writer, sheet_name=sheet_name)
    for sheet_name, sheet_data in campaign_sheets.items():
        csv_filename = os.path.join(output_dir, f"{sheet_name}.csv")  # Updated file path
        sheet_data.to_csv(csv_filename, index=False)  # Saves the sheet as a CSV file
        