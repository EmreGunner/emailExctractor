import pandas as pd
import os
from urllib.parse import urlparse
import sqlite3
#print(os.getcwd())

def extracted_domain(url):
    try:
        if pd.isna(url) or not url:
            return None
        url = url.strip().lower()
        parsed_url = urlparse(url)
        domain = parsed_url.netloc
        domain = domain.split('@')[-1]  # Remove user info if present
        domain = domain.split(':')[0]  # Remove port if present
        domain = domain.replace('www.', '')  # Consistently remove 'www.'
        return domain
    except Exception as e:
        print(f"Error extracting domain from {url}: {e}")
        return None

# The merging function remains the same

def merge_dfs_on_domain(primary_df, secondary_df):
    """
    Merge two DataFrames on a 'domain' column.

    :param primary_df: DataFrame to be merged (main DataFrame).
    :param secondary_df: DataFrame to merge with.
    :return: Merged DataFrame.
    """
  # Apply domain extraction to both DataFrames
    primary_df['domain'] = primary_df['website'].apply(extracted_domain)
    secondary_df['domain'] = secondary_df['website'].apply(extracted_domain)

    # Merge the DataFrames
    merged_df = pd.merge(primary_df, secondary_df, on='domain', how='left')

    return merged_df
def merge_emails(df1, df2):
    # Merge df1 into df2 on the matching domains
    merged_df = pd.merge(df2, df1, how='left', left_on='extracted_domain', right_on='domain')


     # Group by extracted_domain and aggregate emails, then join this back to df2
    aggregated_emails = merged_df.groupby('extracted_domain')['email'].apply(lambda x: ','.join(x.dropna().unique())).reset_index()
    aggregated_emails.rename(columns={'email': 'emails'}, inplace=True)
     # Merge the aggregated emails back into df2
    final_df = pd.merge(df2, aggregated_emails, on='extracted_domain', how='left')
    
    return final_df
def fill_missing_domains(email_df):
    # Check for missing 'domain' values and fill them using 'website'
    missing_domains = email_df['domain'].isna()
    email_df.loc[missing_domains, 'domain'] = email_df.loc[missing_domains, 'website'].apply(extracted_domain)
    return email_df

    
def read_sql_table(query):
    # Create your connection.
    conn = sqlite3.connect('website_leads.db')
    df = pd.read_sql_query(query, conn)
    conn.close()  
    return df
    

def vlookup_mails(df1,df2):
    # Fill missing domains in df1 (email_table) before merging
    df1 = fill_missing_domains(df1)

    if df2 is not None:
        df2['extracted_domain'] = df2['website'].apply(extracted_domain)
        #print(df2.head())  # Display the first few rows of the dataframe
    # Merge emails from df1 into df2
    df2 = merge_emails(df1, df2)
    return df2
    
if __name__ == "__main__":
    # Define file paths (consider replacing these with command-line arguments or a config file)
    #df1 = pd.read_csv(path1)
    #df2 = pd.read_csv(path2)
    email_table = read_sql_table("SELECT * FROM emails")
    gmaps_table = read_sql_table("SELECT * FROM gmaps_lawyers_all")
    print("gmaps table_count: ",gmaps_table.count())
    merged_Df = vlookup_mails(email_table,gmaps_table)
    print(merged_Df)
    #output_file = 'merged_output.csv'  # Define your desired output file name
    # Set index=False to not include the index in the CSV

    #merged_Df.to_csv(output_file,index=False)