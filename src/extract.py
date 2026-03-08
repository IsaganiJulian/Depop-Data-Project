import os
from argparse import ArgumentParser
from pathlib import Path

import pandas as pd
from supabase import create_client

STORAGE_BUCKET = "raw-data"


def _download_folder(client, bucket: str, folder_path: str, dest: Path) -> int:
    """Recursively download CSV files from a bucket folder into dest (flat).

    Supabase Storage folders have id=None in the listing response.
    All CSVs are written flat into dest regardless of subfolder depth.
    """
    items = client.storage.from_(bucket).list(folder_path)
    count = 0
    for item in items:
        name = item["name"]
        full_path = f"{folder_path}/{name}" if folder_path else name
        if item.get("id") is None:
            # It's a subfolder — recurse into it
            count += _download_folder(client, bucket, full_path, dest)
        elif name.endswith(".csv"):
            data = client.storage.from_(bucket).download(full_path)
            (dest / name).write_bytes(data)
            print(f"  Downloaded: {full_path}")
            count += 1
    return count


def download_raw_files(
    raw_data_path: str = "data/raw",
    bucket: str = STORAGE_BUCKET,
) -> None:
    """Download all CSV files from Supabase Storage into the raw data directory.

    Walks the entire bucket recursively, so files organised into year-based
    subfolders (e.g. 2024/, 2025/) are all downloaded correctly.
    """
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    if not url or not key:
        raise EnvironmentError("SUPABASE_URL and SUPABASE_KEY must be set.")

    client = create_client(url, key)
    dest = Path(raw_data_path)
    dest.mkdir(parents=True, exist_ok=True)

    total = _download_folder(client, bucket, folder_path="", dest=dest)
    if total == 0:
        raise FileNotFoundError(f"No CSV files found in Supabase Storage bucket '{bucket}'.")

    print(f"Downloaded {total} file(s) from bucket '{bucket}' → {dest}")


def extract_data(raw_data_path: str = "data/raw") -> pd.DataFrame:
    """Extract and combine all CSV files from a raw data directory."""
    csv_files = sorted(Path(raw_data_path).glob("*.csv"))
    if not csv_files:
        raise FileNotFoundError(f"No CSV files found in: {raw_data_path}")

    dataframe_list = [pd.read_csv(file_path) for file_path in csv_files]
    combined_df = pd.concat(dataframe_list, ignore_index=True)
    print(f"Extracted {len(combined_df)} rows from {len(csv_files)} files.")
    return combined_df


def write_combined_csv(
    raw_data_path: str = "data/raw",
    output_path: str = "data/processed/combined.csv",
) -> pd.DataFrame:
    """Run extraction and write combined output CSV."""
    combined_df = extract_data(raw_data_path=raw_data_path)
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    combined_df.to_csv(output, index=False)
    print(f"Wrote combined data to: {output}")
    return combined_df


def _build_parser() -> ArgumentParser:
    parser = ArgumentParser(description="Combine Depop raw CSV exports.")
    parser.add_argument(
        "--raw-data-path",
        default="data/raw",
        help="Directory containing raw CSV files.",
    )
    parser.add_argument(
        "--output-path",
        default="data/processed/combined.csv",
        help="Location for combined CSV output.",
    )
    return parser


if __name__ == "__main__":
    args = _build_parser().parse_args()
    df = write_combined_csv(
        raw_data_path=args.raw_data_path,
        output_path=args.output_path,
    )
    print(df.head())
