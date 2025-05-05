import pandas as pd
import sqlite3

df = pd.read_csv('data/processed/cleaned.csv')
conn = sqlite3.connect('data/processed/sales.db')
df.to_sql('sales', conn, if_exists='replace', index=False)
conn.close()
print("Database loaded at: data/processed/sales.db")