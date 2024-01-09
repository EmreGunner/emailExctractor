from merged_result_play import *
import pandas as pd
from verify_email import verify_email
from tqdm import tqdm
import multiprocessing

excel_file_path = 'campaign_sheets.xlsx'  # Update this path if needed

excluded_domains = [
    'adresiniz.com', 'godaddy.com', 'example.com', 'yoursite.com', 
    'your-domain.com', 'sirketiniz.com', 'sentry.wixpress.com', 'ornek.com'
]
excluded_extensions = ['.jpeg', '.jpg', '.png']

# Function to verify email
def check_email_verification(email):
    try:
        return verify_email(email)
    except Exception as e:
        print(f"Error verifying email {email}: {e}")
        return False

def process_emails(emails):
    with multiprocessing.Pool() as pool:
        results = list(tqdm(pool.imap(check_email_verification, emails), total=len(emails)))
    return results

# Load all sheets from the Excel file
xls = pd.ExcelFile(excel_file_path)
sheet_names = xls.sheet_names

# Prepare output Excel file
output_excel_path = 'filtered_campaign_sheets.xlsx'  # Define the output Excel file path
def main():
    xls = pd.ExcelFile(excel_file_path)
    sheet_names = xls.sheet_names
    output_excel_path = 'filtered_campaign_sheets.xlsx'
    with pd.ExcelWriter(output_excel_path) as writer:
        for sheet_name in sheet_names:
            df_filtered = pd.read_excel(xls, sheet_name)

            # Apply add_columns and filter_by_email_domain functions
            df_filtered = add_columns(df_filtered)
            df_filtered = filter_by_email_domain(df_filtered, excluded_domains, excluded_extensions)

            # Add email verification status with progress bar
            #tqdm.pandas(desc=f"Verifying emails in {sheet_name}")
            #df_filtered['email_verify_status'] = df_filtered['email'].progress_apply(check_email_verification)

            # Process emails in parallel using multiprocessing
            email_verification_results = process_emails(df_filtered['email'])
            df_filtered['email_verify_status'] = email_verification_results

            # Save the filtered DataFrame to a sheet in the output Excel file
            df_filtered.to_excel(writer, sheet_name=sheet_name, index=False)

print(f"Filtered data saved to {output_excel_path}")