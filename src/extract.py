from argparse import ArgumentParser
from pathlib import Path

import pandas as pd


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
