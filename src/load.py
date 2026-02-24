from argparse import ArgumentParser
from pathlib import Path
import sqlite3

import pandas as pd


def load_to_sqlite(
    input_path: str = "data/processed/cleaned.csv",
    db_path: str = "data/processed/sales.db",
    table_name: str = "sales",
) -> pd.DataFrame:
    """Load cleaned CSV into a SQLite table."""
    source = Path(input_path)
    if not source.exists():
        raise FileNotFoundError(f"Input file not found: {source}")

    db_file = Path(db_path)
    db_file.parent.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(source)
    with sqlite3.connect(db_file) as conn:
        df.to_sql(table_name, conn, if_exists="replace", index=False)

    print(f"Database loaded at: {db_file} (table: {table_name})")
    return df


def _build_parser() -> ArgumentParser:
    parser = ArgumentParser(description="Load cleaned Depop CSV into SQLite.")
    parser.add_argument(
        "--input-path",
        default="data/processed/cleaned.csv",
        help="Path to cleaned CSV file.",
    )
    parser.add_argument(
        "--db-path",
        default="data/processed/sales.db",
        help="Path to SQLite database file.",
    )
    parser.add_argument(
        "--table-name",
        default="sales",
        help="Destination table name.",
    )
    return parser


if __name__ == "__main__":
    args = _build_parser().parse_args()
    df = load_to_sqlite(
        input_path=args.input_path,
        db_path=args.db_path,
        table_name=args.table_name,
    )
    print(df.info())
