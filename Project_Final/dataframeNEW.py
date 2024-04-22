# %%
import json
import pandas as pd   
import yaml
import numpy as np
import sqlite3
import sqlalchemy
from sqlalchemy import create_engine
data = []
c = 0

with open('Data_Clothing_Nine_Thousand_entries.jsonl') as f:
    for line in f:
        data.append(json.loads(line))
        c+=1        
        if c == 17000:
            break

data_df = pd.DataFrame(data)
data_df['gender'] = data_df['categories'].str[1]
data_df['type'] = data_df['categories'].str[2]
data_df['misc'] = data_df['categories'].str[3]

data_df = data_df.drop(['features', 'images', 'description', 'videos', 'categories', 'parent_asin', 'details', 'bought_together', 'subtitle', 'author'], axis=1)

data_df.dropna(subset=['price'], inplace=True)

data_df.reset_index(inplace = True, drop=False)
data_df.rename(columns={'index': "id"})

data_full = data_df[["index", "main_category", "title", "average_rating", "rating_number", "price", "store", "gender", "type", "misc"]]

engine = create_engine('sqlite:///instance/amazon.db')
data_full.to_sql('Inventory', con=engine, index=False, if_exists='replace')
cust_stats_f = data_df[["customer_id", "total_orders", "total_items", "total_spent"]]




