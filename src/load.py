import os
from pathlib import Path

import pandas as pd
from supabase import create_client

TABLE_NAME = "sales"
BATCH_SIZE = 500  # rows per upsert request — stays well under Supabase limits

# Maps cleaned CSV headers → Postgres snake_case column names.
# Power BI's PostgreSQL connector will surface these names directly.
COLUMN_MAP = {
    "Date of sale":              "date_of_sale",
    "Time of sale":              "time_of_sale",
    "Date of listing":           "date_of_listing",
    "Bundle":                    "bundle",
    "Brand":                     "brand",
    "Description":               "description",
    "Size":                      "size",
    "Item price":                "item_price",
    "Buyer shipping cost":       "buyer_shipping_cost",
    "Total":                     "total",
    "Depop fee":                 "depop_fee",
    "Depop Payments fee":        "depop_payments_fee",
    "Boosting fee":              "boosting_fee",
    "Payment type":              "payment_type",
    "Category":                  "category",
    "City":                      "city",
    "State":                     "state",
    "Post Code":                 "post_code",
    "Country":                   "country",
    "US Sales tax":              "us_sales_tax",
    "Refunded to buyer amount":  "refunded_to_buyer_amount",
    "Fees refunded to seller":   "fees_refunded_to_seller",
    "order_id":                  "order_id",
    "time_to_sell_days":         "time_to_sell_days",
}


def _get_client():
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    if not url or not key:
        raise EnvironmentError(
            "SUPABASE_URL and SUPABASE_KEY environment variables must be set."
        )
    return create_client(url, key)


def load_to_supabase(
    input_path: str = "data/processed/cleaned.csv",
    table_name: str = TABLE_NAME,
) -> pd.DataFrame:
    """Load cleaned CSV into Supabase via batched upsert on order_id.

    Re-running the pipeline is safe: existing rows are updated in place
    rather than duplicated, because the upsert conflicts on order_id.
    """
    source = Path(input_path)
    if not source.exists():
        raise FileNotFoundError(f"Input file not found: {source}")

    df = pd.read_csv(source)

    # Rename to snake_case for Postgres / Power BI
    df = df.rename(columns=COLUMN_MAP)

    # Serialise date columns to ISO strings (JSON-safe)
    for col in ("date_of_sale", "date_of_listing"):
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce").dt.strftime("%Y-%m-%d")

    # Convert time_to_sell_days to plain int where possible
    if "time_to_sell_days" in df.columns:
        df["time_to_sell_days"] = pd.to_numeric(
            df["time_to_sell_days"], errors="coerce"
        ).astype("Int64")

    # Replace NaN / NaT with None so records serialise to valid JSON
    df = df.where(pd.notnull(df), other=None)

    client = _get_client()
    records = df.to_dict(orient="records")
    total = len(records)

    for start in range(0, total, BATCH_SIZE):
        batch = records[start : start + BATCH_SIZE]
        client.table(table_name).upsert(batch, on_conflict="order_id").execute()
        print(f"  Upserted rows {start + 1}–{min(start + BATCH_SIZE, total)} / {total}")

    print(f"Loaded {total:,} rows into Supabase table '{table_name}'.")
    return df
