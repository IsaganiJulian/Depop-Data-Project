# Depop-ETL

## Project Overview

Depop-ETL is an automated data engineering pipeline for extracting, cleaning, and loading sales data from CSV files into a SQLite database. Designed for e-commerce analytics, the project streamlines the process of preparing raw sales data (such as from Depop) for robust, SQL-based analysis and reporting.

## Features

- **Automated ETL Pipeline:** Extracts raw sales data from CSV, cleans and standardizes it, and loads it into a SQLite database with a single command.
- **Comprehensive Data Cleaning:** Handles missing values, standardizes state names, converts data types, removes sensitive information, and eliminates duplicates using modular Python classes.
- **Database Integration:** Loads cleaned data into a normalized SQLite database (`sales.db`), enabling efficient SQL queries and downstream analytics.
- **Reproducible & Documented:** Modular code structure, clear documentation, and version control with Git for easy maintenance and collaboration.
- **Analysis-Ready:** Supports Jupyter notebook-based exploration and reporting on the processed data.

---
## Project Structure
```
├── config/ # Configuration files
├── data/ # Data files
│ ├── processed/
│ └── raw/
├── notebooks/ # Jupyter notebooks for exploration
├── reports/ # Analysis reports or logs
├── src/ # Python scripts (ETL pipeline)
│ ├── init.py
│ ├── extract.py
│ ├── load.py
│ └── transform.py
├── tests/ # Unit tests
├── .gitignore
└── README.md
```

> **Note:** The `data/raw/` directory is excluded from version control to protect sensitive customer information. Please add your own raw CSV files to `data/raw/` to use this project.

## Getting Started

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)
- [pandas](https://pandas.pydata.org/) and [sqlite3](https://docs.python.org/3/library/sqlite3.html) libraries

### Installation

1. **Clone the repository:**
    ```
    git clone https://github.com/your-username/Depop-ETL.git
    cd Depop-ETL
    ```

2. **Create and activate a virtual environment (recommended):**
    ```
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Install dependencies:**
    ```
    pip install pandas
    ```

---

## Usage

1. **Add your raw CSV sales files** to the `data/raw/` directory.

2. **Run the ETL pipeline scripts:**
    - Extract: `python src/extract.py`
    - Transform: `python src/transform.py`
    - Load: `python src/load.py`

3. **Check the SQLite database** (created automatically).

4.  **Explore your data** using Jupyter notebooks in the `notebooks/` directory or run SQL queries using DB Browser for SQLite.

---

## Example SQL Queries
-- Total sales
SELECT COUNT(*) FROM sales;

-- Revenue by state
SELECT State, SUM("Item price") AS revenue FROM sales GROUP BY State ORDER BY revenue DESC;

-- Top 5 sales
SELECT * FROM sales ORDER BY "Item price" DESC LIMIT 5;

---
## Example Workflow

Step 1: Extract data from CSVs  
`python src/extract.py`

Step 2: Transform/clean the data  
`python src/transform.py`

Step 3: Load cleaned data into SQLite  
`python src/load.py`

---

## Future Improvements

- Automate CSV downloads from Depop or other sources
- Add logging and error handling
- Schedule ETL jobs with cron or Airflow
- Add data validation and unit tests

---

## License

This project is licensed under the MIT License.

---

## Author

Created by [Isagani Hernandez](https://github.com/IsaganiJulian).  
Feel free to reach out with questions or suggestions!
