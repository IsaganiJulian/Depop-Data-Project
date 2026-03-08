import pandas as pd

REQUIRED_COLUMNS = ['Date of sale', 'Item price', 'State', 'Total', 'order_id']


def quality_checks(df: pd.DataFrame) -> bool:
    passed = True

    # 1. Required columns exist
    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        print(f"Quality check FAILED — missing columns: {missing}")
        passed = False
    else:
        print("All required columns present.")

    # 2. Item price and Total are numeric and non-negative
    for col in ['Item price', 'Total']:
        if col not in df.columns:
            continue
        if not pd.api.types.is_numeric_dtype(df[col]):
            print(f"Quality check FAILED — {col} is not numeric.")
            passed = False
        elif (df[col] < 0).any():
            print(f"Quality check FAILED — {col} contains negative values.")
            passed = False
        else:
            print(f"{col} looks good.")

    # 3. order_id is unique
    if 'order_id' in df.columns:
        if df['order_id'].duplicated().any():
            print("Quality check FAILED — order_id has duplicates.")
            passed = False
        else:
            print("order_id is unique.")

    # 4. Duplicate row count
    dup_count = df.duplicated().sum()
    print(f"Duplicate row count: {dup_count}")

    # 5. Null rate report for key columns
    for col in ['Item price', 'State', 'Date of sale', 'Total']:
        if col in df.columns:
            null_rate = df[col].isnull().mean() * 100
            print(f"Null rate for {col}: {null_rate:.2f}%")

    return passed
