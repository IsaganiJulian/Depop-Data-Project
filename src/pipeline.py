from extract import write_combined_csv
from load import load_to_sqlite
from transform import write_cleaned_csv


def run_pipeline() -> None:
    """Run full ETL pipeline end-to-end."""
    write_combined_csv()
    write_cleaned_csv()
    load_to_sqlite()
    print("ETL pipeline completed successfully.")


if __name__ == "__main__":
    run_pipeline()
