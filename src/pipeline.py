from extract import write_combined_csv
from load import load_to_sqlite
from transform import write_cleaned_csv
from src.quality import quality_checks 

def run_pipeline() -> None:
    """Run full ETL pipeline end-to-end."""
    write_combined_csv()
    write_cleaned_csv()
    df = pd.read_csv('../data/processed/cleaned.csv')  # Adjust path if needed
    if quality_checks(df):  # Assume quality_checks returns True/False
        load_to_sqlite()
        print("ETL pipeline completed successfully.")
    else:
        print("Quality validation failed. Pipeline stopped.")
    load_to_sqlite()
   
    print("ETL pipeline completed successfully.")


if __name__ == "__main__":
    run_pipeline()
