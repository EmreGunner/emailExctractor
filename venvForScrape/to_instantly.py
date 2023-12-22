import sqlite3
import pandas as pd
from pandas_merger import merge_dfs_on_domain

# Create your connection.
conn = sqlite3.connect('website_leads.db')
not_send_df = pd.read_sql_query("SELECT * FROM emails WHERE status <> 1 OR status IS NULL AND email <> '' AND email IS NOT NULL", conn)
gmaps_lawyers_df = pd.read_sql_query("SELECT * FROM gmaps_lawyers_all",conn)
print("Not send  :",not_send_df.head())
print("Gmaps  :",gmaps_lawyers_df.head())
merged_df = merge_dfs_on_domain(not_send_df,gmaps_lawyers_df)
print(merged_df)
#merged_Df = vlookup_mails(not_send_df,gmaps_lawyers_df)
print(merged_df)
merged_df.to_csv("test2.csv",index=None)
