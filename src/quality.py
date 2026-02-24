import pandas as pd

REQUIRED_COLUMNS = ['Date of sale', 'Item price', 'State', 'Total', 'order_id']

def quality_checks(df);
    #1. Required columns exist
    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        print(f"Missing columns: {missing}")
    else:
        print(f"All required columns present.")

    #2. Item price and Total are numeric and non-negative
    for col in ['Item price', 'Total']:
        if not pd.api.types.is_numeric_dtype(df(col));
            print(f"{col} is not numeric.")
        elif (df[col] < 0).any():
            print(f"{col} contains negative values.")
        else:
            print(f"{col} looks good.")
    
    # 3. order_id is unique
    if df['order_id'].duplicated().any():
        print("order_id has duplicates.")
    else:
        print("order_id is unique.")
    
     # 4. Duplicate row count
    dup_count = df.duplicated().sum()
    print(f"Duplicate row count: {dup_count}")

    # 5. Null rate report for key columns
    for col in ['Item price', 'State', 'Date of sale', 'Total']:
        null_rate = df[col].isnull().mean() * 100
        print(f"Null rate for {col}: {null_rate:.2f}%")