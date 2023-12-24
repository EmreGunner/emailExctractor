import pandas as pd
import os
from db_functionsV2 import check_value
from db_functionsV2 import update_status_in_db
outreached_list = []

def get_alraedy_outreach():
    for website in df['website']:
        print(f"checking the status: of website {website}")
        outreached_list.append(website)
        # Check if the website is in the database
        exists = check_value(website, 'website', 'emails')
        # Update the status in the database
        update_status_in_db(website, 1 if exists else 0)
    return outreached_list

input_file = "/home/titan/Desktop/Bussiness/SoftwareTools/LeadGeneration/EmailExtractor/venvForScrape/input/instantly_leads (1).csv"
df = pd.read_csv(input_file)

outreached_data = get_alraedy_outreach()
print(outreached_data)



