import pandas as pd
import glob 
import os

def extract_data(raw_data_path="data/raw"):
    """Extracts and combines all CSV files from the raw data directory."""
    all_files = glob.glob(os.path.join(raw_data_path, "*.csv"))
    df_list = [pd.read_csv(f) for f in all_files]
    if df_list:
        df = pd.concat(df_list, ignore_index=True)
        print(f"Extracted {len(df)} rows from {len(all_files)} files.")
        return df 
    else:
        print("No CSV files found in the raw data directory.")
        return pd.DataFrame()
    
if __name__ == "__main__":
    df = extract_data()
    df.to_csv("data/processed/combined.csv", index=False)
    print(df.head())
