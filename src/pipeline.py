import os
import sys

import pandas as pd

from extract import download_raw_files, write_combined_csv
from load import load_to_supabase
from transform import write_cleaned_csv
from quality import quality_checks


# ---------------------------------------------------------------------------
# Paths — resolved relative to the repo root so the script can be invoked
# from anywhere: `python src/pipeline.py` or `python -m src.pipeline`.
# ---------------------------------------------------------------------------
_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_CLEANED_CSV = os.path.join(_REPO_ROOT, "data", "processed", "cleaned.csv")
_RAW_DATA_PATH = os.path.join(_REPO_ROOT, "data", "raw")
_COMBINED_CSV = os.path.join(_REPO_ROOT, "data", "processed", "combined.csv")


def run_pipeline() -> None:
    """Run full ETL pipeline end-to-end."""
    print("=== Depop ETL Pipeline starting ===")

    # Download raw CSVs from Supabase Storage (never stored in git)
    download_raw_files(raw_data_path=_RAW_DATA_PATH)

    # Extract
    write_combined_csv(raw_data_path=_RAW_DATA_PATH, output_path=_COMBINED_CSV)

    # Transform
    write_cleaned_csv(input_path=_COMBINED_CSV, output_path=_CLEANED_CSV)

    # Quality checks
    df = pd.read_csv(_CLEANED_CSV)
    if not quality_checks(df):
        print("Quality validation FAILED. Pipeline stopped.")
        sys.exit(1)

    # Load
    load_to_supabase(input_path=_CLEANED_CSV)

    # Summary
    print(f"=== Pipeline completed successfully — {len(df):,} rows loaded ===")


if __name__ == "__main__":
    run_pipeline()
