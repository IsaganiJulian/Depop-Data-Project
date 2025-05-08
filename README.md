# Depop Data Analytics
> **Note:** This project is a work in progress. Features, analysis, and documentation are being actively developed and improved.
> 
> **Last Updated:** May 8, 2025

## Project Status

- ✅ ETL Pipeline: Completed
- 🔄 Data Analysis: In Progress
- ⏳ Data Science (Modeling): Planned / Upcoming
- 📊 Dashboards: Planned / Upcoming

---

## Project Overview

Depop Data Analytics is a comprehensive, end-to-end data project built on real-world e-commerce sales data from Depop. This repository demonstrates the full data workflow, including:

- **Automated ETL (Extract, Transform, Load):** Clean and structure raw sales data for robust, SQL-based analysis.
- **Data Analysis & Visualization:** Explore, visualize, and report on sales trends, customer behavior, and business insights.
- **Data Science:** Apply machine learning to solve business problems and generate predictive insights.

All sensitive customer information (names, usernames, addresses) has been removed or anonymized to ensure privacy.

---

## Features

- **Automated ETL Pipeline:** Extracts raw sales data from CSV, cleans and standardizes it, and loads it into a SQLite database with a single command.
- **Comprehensive Data Cleaning:** Handles missing values, standardizes state names, converts data types, removes sensitive information, and eliminates duplicates using modular Python classes.
- **Database Integration:** Loads cleaned data into a normalized SQLite database (`sales.db`), enabling efficient SQL queries and downstream analytics.
- **Reproducible & Documented:** Modular code structure, clear documentation, and version control with Git for easy maintenance and collaboration.
- **Analysis-Ready:** Supports Jupyter notebook-based exploration and reporting on the processed data.
- **Data Analysis & Visualization:** Example notebooks and Tableau dashboards for exploring trends and generating insights.
- **Data Science Workflows:** Notebooks for feature engineering, modeling, and evaluation.

---

## Table of Contents

1. [Project Structure](#project-structure)  
2. [ETL Pipeline](#etl-pipeline)  
3. [Data Analysis](#data-analysis)  
4. [Data Science](#data-science)  
5. [Dashboards](#dashboards)  
6. [SQL Queries](#sql-queries)  
7. [Getting Started](#getting-started)  
8. [Usage](#usage)  
9. [Example Workflow](#example-workflow)  
10. [Future Improvements](#future-improvements)  
11. [License](#license)  
12. [Author](#author)  

---
## Project Structure
```
├── analysis/
│ ├── notebooks/ # Jupyter notebooks for EDA & visualization
│ └── reports/ # Analysis summary reports
├── config/ # Configuration files
├── dashboards/ # Tableau or BI dashboards
├── data/
│ ├── processed/ # Cleaned, analysis-ready data
│ └── raw/ # Raw Depop sales data (not included for privacy)
├── data_science/
│ ├── notebooks/ # ML modeling, feature engineering, evaluation
│ └── reports/ # Model results & business insights
├── sql/
│ ├── eda/ # Exploratory Data Analysis queries
│ ├── transform/ # Data cleaning and transformation queries
│ └── reporting/ # Reporting/dashboard queries (for Tableau, etc.)
├── src/ # Python scripts (ETL pipeline)
│ ├── extract.py
│ ├── init.py
│ ├── load.py
│ └── transform.py
├── tests/ # Unit tests
├── .gitignore
└── README.md
```

> **Note:** The `data/raw/` directory is excluded from version control to protect sensitive customer information. Please add your own raw CSV files to `data/raw/` to use this project.

---

## SQL Queries

All SQL queries used in the project are organized in the `sql/` directory for clarity, reusability, and integration with Python and Tableau.

- **`sql/eda/`**: Queries for exploratory data analysis (e.g., data overview, summary statistics, missing values).  
- **`sql/transform/`**: Data cleaning and transformation queries (e.g., handling nulls, type conversions).  
- **`sql/reporting/`**: Queries used for reporting and dashboards (e.g., revenue by state, top products).

**Best Practices:**

- Each query is saved in a separate, clearly-named `.sql` file.  
- Queries include a commented header with a description, author, and last modified date.  
- SQL code is formatted for readability and maintainability (keywords capitalized, each clause on a new line, meaningful aliases).

**Example SQL file header:**
-- File: eda_total_sales.sql
-- Description: Returns the total number of sales in the sales table.
-- Author: Isagani Hernandez
-- Last Modified: 2025-05-08

---
### Using SQL Queries in Python

You can load and execute queries from the `sql/` directory in your Python scripts or notebooks:

with open('sql/eda/eda_total_sales.sql') as f:
query = f.read()
df = pd.read_sql_query(query, conn)

---

### Using SQL Queries in Tableau

_Reporting queries for Tableau dashboards will be added as the project progresses._

---

## Example SQL Queries

Below are examples of the types of queries stored in the `sql/` directory. For maintainability, use the actual `.sql` files in your workflow.



## ETL Pipeline

**Goal:** Automate the cleaning and loading of raw Depop sales data into a structured SQLite database for downstream analysis.

- Scripts in `src/` handle data extraction, cleaning, transformation, and loading.
- Sensitive fields (buyer names, usernames, addresses) are removed or anonymized.
- Output: Cleaned CSV and SQLite database in `data/processed/`.

---

## Data Analysis

**Goal:** Explore and visualize sales data to uncover trends and actionable insights.

- **Notebooks in `analysis/notebooks/`:**
    - `01_eda.ipynb`: Data overview, summary statistics, missing values
    - `02_sales_trends.ipynb`: Sales over time, by product, by region
    - `03_customer_analysis.ipynb`: Customer segmentation and behavior
- **Reports in `analysis/reports/`:**
    - Summary of key findings and visualizations
- **Automated Tableau Dashboard:**
    - Interactive dashboard for business users (see [Dashboards](#dashboards) below)

---

## Data Science

**Goal:** Apply machine learning to solve business problems and generate predictive insights.

- **Notebooks in `data_science/notebooks/`:**
    - `01_feature_engineering.ipynb`: Feature selection and creation
    - `02_modeling.ipynb`: Model training (e.g., sales forecasting, customer segmentation)
    - `03_evaluation.ipynb`: Model evaluation and interpretation
    - `04_deployment.ipynb`: (Optional) Example of model deployment or scoring
- **Reports in `data_science/reports/`:**
    - Model performance, feature importance, and business recommendations

---

## Dashboards

- **Tableau Dashboard:**  
  [View Interactive Dashboard on Tableau Public](YOUR_TABLEAU_LINK_HERE)
- Dashboard is automatically updated from the latest processed data.
- Visualizes sales trends, product performance, and customer insights.

---

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

4.  **Explore your data** using Jupyter notebooks in the `analysis/notebooks/` or `notebooks/` directory, or run SQL queries using DB Browser for SQLite.

---

## Example SQL Queries
-- Total sales
SELECT COUNT(*) FROM sales;

-- Revenue by state
SELECT State, SUM("Item price") AS revenue FROM sales GROUP BY State ORDER BY revenue DESC;

-- Top 5 sales
SELECT * FROM sales ORDER BY "Item price" DESC LIMIT 5;

---

## Future Improvements

- Automate CSV downloads from Depop or other sources
- Add logging and error handling
- Schedule ETL jobs with cron or Airflow
- Add data validation and unit tests
- Expand data science models and business use cases

---

## License

This project is licensed under the MIT License.

---

## Author

Created by [Isagani Hernandez](https://github.com/IsaganiJulian).  
Feel free to reach out with questions or suggestions!
