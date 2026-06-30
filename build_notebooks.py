#!/usr/bin/env python3
# =============================================================================
# build_notebooks.py
# =============================================================================
# DVLA Ghana Big Data Practical Lab — Multi-Tenant Jupyter Notebook Builder
#
# Purpose:
#   Programmatically generates valid .ipynb Jupyter Notebook files for each
#   of the four lab workspaces (kevin, benjamin, albert, peter). Each workspace
#   receives three notebooks:
#     1. Lab0_Big_Data_SQL_and_ETL_Basics.ipynb   (Big Data, SQL, and ETL Basics)
#     2. Lab1_SQL_Profiling_and_Extraction.ipynb  (DuckDB SQL profiling)
#     3. Lab2_PySpark_ETL_and_Transformation.ipynb (PySpark ETL pipeline)
#
#   Kevin's workspace is the instructor's pre-flight validation environment.
#   The three student workspaces are identical in content but personalized
#   with each student's name.
#
# Usage:
#   python build_notebooks.py
#
# Author:  Lab Infrastructure (auto-generated)
# Date:    June 2026
# =============================================================================

import os
import json

# =============================================================================
# CONFIGURATION
# =============================================================================

# Base directory (where this script lives)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Workspace profiles: (folder_name, display_name, role)
WORKSPACES = [
    ("kevin", "Kevin", "Lab Instructor"),
    ("benjamin", "Benjamin Y. Peh", "Manager, MIS"),
    ("albert", "Albert Wotorgbui", "Deputy Director"),
    ("peter", "Peter Djameshie", "Officer"),
]


# =============================================================================
# NOTEBOOK JSON STRUCTURE HELPERS
# =============================================================================

def create_notebook_skeleton() -> dict:
    """
    Create a valid Jupyter Notebook v4.5 JSON skeleton.

    The notebook format specification requires:
      - nbformat: 4 (major version)
      - nbformat_minor: 5 (minor version — supports cell IDs)
      - metadata: must contain a kernelspec defining the Python 3 kernel
      - cells: list of cell objects (markdown or code)

    Returns:
        A dictionary representing an empty, valid .ipynb structure.
    """
    return {
        "nbformat": 4,
        "nbformat_minor": 5,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3 (ipykernel)",
                "language": "python",
                "name": "python3",
            },
            "language_info": {
                "name": "python",
                "version": "3.12.0",
                "mimetype": "text/x-python",
                "file_extension": ".py",
            },
        },
        "cells": [],
    }


def make_markdown_cell(source_lines: list) -> dict:
    """
    Create a Jupyter markdown cell.

    Parameters:
        source_lines: List of strings, each representing a line of markdown.
                      Lines should NOT include trailing newlines — they are
                      added automatically.

    Returns:
        A dictionary representing a valid Jupyter markdown cell.
    """
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": [line + "\n" for line in source_lines[:-1]] + [source_lines[-1]],
    }


def make_code_cell(source_lines: list) -> dict:
    """
    Create a Jupyter code cell.

    Parameters:
        source_lines: List of strings, each representing a line of Python code.
                      These are the template/placeholder lines that students
                      will see when they open the notebook.

    Returns:
        A dictionary representing a valid Jupyter code cell with empty outputs.
    """
    return {
        "cell_type": "code",
        "metadata": {},
        "source": [line + "\n" for line in source_lines[:-1]] + [source_lines[-1]],
        "outputs": [],
        "execution_count": None,
    }


def save_notebook(notebook: dict, filepath: str) -> None:
    """
    Save a notebook dictionary as a .ipynb JSON file.

    Parameters:
        notebook: The notebook dictionary structure.
        filepath: Absolute path where the .ipynb file will be written.
    """
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(notebook, f, indent=1, ensure_ascii=False)
    print(f"  [OK] Saved: {filepath}")


# =============================================================================
# LAB 0: BIG DATA, SQL AND ETL BASICS (DuckDB & Pandas)
# =============================================================================

def build_lab0(student_name: str, role: str, student_folder: str) -> dict:
    """
    Build Lab0_Big_Data_SQL_and_ETL_Basics.ipynb.

    This notebook introduces absolute beginners to:
      1. Big Data concepts (OLTP vs OLAP, columnar formats)
      2. SQL Querying basics using DuckDB
      3. ETL concepts using Python & Pandas

    Parameters:
        student_name:   The student's display name for personalization.
        role:           The student's job role/title.
        student_folder: The student's workspace folder name.

    Returns:
        A complete notebook dictionary ready to be saved as .ipynb.
    """
    nb = create_notebook_skeleton()
    cells = nb["cells"]

    # =========================================================================
    # CELL 1: Welcome & Overview
    # =========================================================================
    cells.append(make_markdown_cell([
        f"# 🎓 Lab 0: Fundamentals of Big Data, SQL & ETL",
        f"",
        f"**Welcome, {student_name}!** ({role})",
        f"",
        f"This introductory lab is designed to give you a strong foundation in the core concepts and tools ",
        f"we will use throughout the training. If you have never written a SQL query or a line of Python code before, ",
        f"do not worry — this lab will guide you step-by-step through every concept.",
        f"",
        f"---",
        f"",
        f"## 📚 Core Concepts Table",
        f"",
        f"| Concept | Description | Why it matters for DVLA Ghana |",
        f"|---|---|---|",
        f"| **Big Data** | Datasets so large or complex that traditional systems cannot handle them efficiently. | DVLA manages millions of vehicle registration and payment records across 20+ branches. |",
        f"| **SQL (Structured Query Language)** | The standard language for communicating with databases to retrieve and summarize data. | Used to query legacy registries and transaction logs to audit records and find leaks. |",
        f"| **ETL (Extract, Transform, Load)** | The process of reading raw data from sources, cleaning/modifying it, and loading it into a target system. | Used to clean raw CSVs from branches, standardize formatting, and prepare data for dashboards. |",
        f"| **OLTP vs. OLAP** | **OLTP** (Online Transaction Processing) is for day-to-day operations (adding a vehicle). **OLAP** (Online Analytical Processing) is for running reports/summaries. | Day-to-day registration systems are OLTP; our audit dashboards are OLAP. |",
    ]))

    # =========================================================================
    # CELL 2: Step 1 — Install & Import Required Libraries
    # =========================================================================
    cells.append(make_markdown_cell([
        f"## Step 1: Install and Import Required Libraries",
        f"",
        f"**📋 What you will do:**",
        f"Install and import **DuckDB** (our database engine) and **Pandas** (our data analysis library).",
        f"",
        f"**🔧 Code to type:**",
        f"```python",
        f"# Install libraries quietly (if not already installed)",
        f"!pip install duckdb pandas --quiet",
        f"",
        f"# Import libraries",
        f"import duckdb",
        f"import pandas as pd",
        f"",
        f"print('DuckDB version:', duckdb.__version__)",
        f"print('Pandas version:', pd.__version__)",
        f"print('✅ Libraries successfully imported!')",
        f"```",
        f"",
        f"**📖 Line-by-line explanation:**",
        f"- `!pip install duckdb pandas --quiet`: Installs the required Python packages.",
        f"- `import duckdb`: Imports DuckDB, which lets us run SQL queries inside our Python code.",
        f"- `import pandas as pd`: Imports Pandas under the shorthand name `pd`. Pandas is the industry standard for working with tables (called DataFrames) in Python.",
        f"",
        f"**💡 Why this matters for DVLA:**",
        f"We will use DuckDB to run fast SQL queries on our raw data, and Pandas to structure, load, and write files in our Python environments.",
    ]))
    cells.append(make_code_cell([
        f"# Step 1: Install and Import Required Libraries",
        f"# Type your code below",
        f"",
    ]))

    # =========================================================================
    # CELL 3: Step 2 — Create In-Memory DB & Practice Tables
    # =========================================================================
    cells.append(make_markdown_cell([
        f"## Step 2: Create an In-Memory Database and Practice Tables",
        f"",
        f"**📋 What you will do:**",
        f"Establish a database connection and create practice tables in memory so you can query them using SQL.",
        f"",
        f"**🔧 Code to type:**",
        f"```python",
        f"# Connect to an in-memory DuckDB database",
        f"con = duckdb.connect()",
        f"",
        f"# Create a practice table for vehicles",
        f"con.execute(\"\"\"",
        f"    CREATE TABLE vehicles (",
        f"        vehicle_id VARCHAR,",
        f"        make VARCHAR,",
        f"        model VARCHAR,",
        f"        year INTEGER,",
        f"        owner_id VARCHAR",
        f"    )",
        f"\"\"\")",
        f"",
        f"# Insert practice records into the vehicles table",
        f"con.execute(\"\"\"",
        f"    INSERT INTO vehicles VALUES",
        f"    ('V101', 'Toyota', 'Corolla', 2018, 'O001'),",
        f"    ('V102', 'Hyundai', 'Elantra', 2020, 'O002'),",
        f"    ('V103', 'Toyota', 'RAV4', 2021, 'O003'),",
        f"    ('V104', 'Honda', 'Civic', 2019, 'O001'),",
        f"    ('V105', 'Nissan', 'Patrol', 2015, 'O004')",
        f"\"\"\")",
        f"",
        f"print('✅ Vehicles table created and populated!')",
        f"```",
        f"",
        f"**📖 Line-by-line explanation:**",
        f"- `con = duckdb.connect()`: Starts an in-process, in-memory database. Since it runs in RAM, no files are written to disk and data resets when the notebook session closes.",
        f"- `con.execute(\"\"\" CREATE TABLE ... \"\"\")`: Executes SQL commands. We define a schema with columns and their types (`VARCHAR` for text, `INTEGER` for whole numbers).",
        f"- `INSERT INTO vehicles VALUES ...`: Adds rows of data to our table.",
        f"",
        f"**💡 Why this matters for DVLA:**",
        f"Creating temporary database connections allows you to verify query syntax and perform test transformations before running operations on real production files.",
    ]))
    cells.append(make_code_cell([
        f"# Step 2: Create In-Memory Database and Practice Tables",
        f"# Type your code below",
        f"",
    ]))

    # =========================================================================
    # CELL 4: Step 3 — Write Your First SQL Query (SELECT, ORDER BY, LIMIT)
    # =========================================================================
    cells.append(make_markdown_cell([
        f"## Step 3: Write Your First SQL Query (SELECT, ORDER BY, LIMIT)",
        f"",
        f"**📋 What you will do:**",
        f"Write a basic query to inspect your tables, order the results, and limit the output size.",
        f"",
        f"**🔧 Code to type:**",
        f"```python",
        f"# Query all rows and columns from the vehicles table",
        f"print('=== ALL VEHICLES ===')",
        f"con.sql('SELECT * FROM vehicles').show()",
        f"",
        f"# Query specific columns, ordered by year descending, limited to 3 rows",
        f"print('=== NEWEST VEHICLES ===')",
        f"con.sql('SELECT make, model, year FROM vehicles ORDER BY year DESC LIMIT 3').show()",
        f"```",
        f"",
        f"**📖 Line-by-line explanation:**",
        f"- `SELECT * FROM vehicles`: The asterisk `*` is a wildcard that means 'retrieve all columns'.",
        f"- `con.sql('...').show()`: Submits the SQL query to DuckDB and formats the result as a printed table.",
        f"- `SELECT make, model, year`: Only pulls these three columns, filtering out the others.",
        f"- `ORDER BY year DESC`: Sorts the rows by the `year` column from highest (newest) to lowest (`DESC` stands for descending).",
        f"- `LIMIT 3`: Ensures that only the top 3 rows are returned. Useful for previewing large datasets.",
        f"",
        f"**💡 Why this matters for DVLA:**",
        f"When dealing with millions of transaction records, you should never load all columns or rows at once. Limiting fields and previewing with `LIMIT` keeps your workspace running fast.",
    ]))
    cells.append(make_code_cell([
        f"# Step 3: Write Your First SQL Query",
        f"# Type your code below",
        f"",
    ]))

    # =========================================================================
    # CELL 5: Step 4 — Filtering Data (WHERE clause)
    # =========================================================================
    cells.append(make_markdown_cell([
        f"## Step 4: Filtering Data (WHERE clause)",
        f"",
        f"**📋 What you will do:**",
        f"Apply the `WHERE` clause to filter out records that do not meet specific criteria.",
        f"",
        f"**🔧 Code to type:**",
        f"```python",
        f"# Filter for Toyota vehicles only",
        f"print('=== TOYOTAS ===')",
        f"con.sql(\"SELECT * FROM vehicles WHERE make = 'Toyota'\").show()",
        f"",
        f"# Filter for vehicles manufactured after 2018",
        f"print('=== POST-2018 VEHICLES ===')",
        f"con.sql(\"SELECT * FROM vehicles WHERE year > 2018\").show()",
        f"```",
        f"",
        f"**📖 Line-by-line explanation:**",
        f"- `WHERE make = 'Toyota'`: Restricts the output to rows where the value in the `make` column is exactly `'Toyota'`. Text literals in SQL are always enclosed in single quotes.",
        f"- `WHERE year > 2018`: Restricts the output to rows where the numeric value in the `year` column is strictly greater than `2018`.",
        f"",
        f"**💡 Why this matters for DVLA:**",
        f"Filtering data allows you to isolate specific branch offices, focus on vehicle makes with high registration rates, or pinpoint anomalies in registration years.",
    ]))
    cells.append(make_code_cell([
        f"# Step 4: Filtering Data",
        f"# Type your code below",
        f"",
    ]))

    # =========================================================================
    # CELL 6: Step 5 — Aggregating & Grouping Data (COUNT, SUM, AVG, GROUP BY)
    # =========================================================================
    cells.append(make_markdown_cell([
        f"## Step 5: Aggregating & Grouping Data (COUNT, SUM, AVG, GROUP BY)",
        f"",
        f"**📋 What you will do:**",
        f"Use aggregate functions to calculate summary metrics and group them by a specific attribute.",
        f"",
        f"**🔧 Code to type:**",
        f"```python",
        f"# Count the total number of vehicles",
        f"con.sql('SELECT COUNT(*) AS total_vehicles FROM vehicles').show()",
        f"",
        f"# Find the count of vehicles grouped by make",
        f"print('=== VEHICLE COUNT BY MAKE ===')",
        f"con.sql('SELECT make, COUNT(*) AS count FROM vehicles GROUP BY make').show()",
        f"```",
        f"",
        f"**📖 Line-by-line explanation:**",
        f"- `COUNT(*)`: Counts the total number of rows that match the query.",
        f"- `AS total_vehicles`: Renames the output column to a clean alias (`total_vehicles`) for readability.",
        f"- `GROUP BY make`: Directs SQL to group identical values in the `make` column together, and run the `COUNT(*)` function for each unique group.",
        f"",
        f"**💡 Why this matters for DVLA:**",
        f"Grouping and aggregating are fundamental to analytics. We use it to count total payments per branch or calculate average registration fees by area code.",
    ]))
    cells.append(make_code_cell([
        f"# Step 5: Aggregating & Grouping Data",
        f"# Type your code below",
        f"",
    ]))

    # =========================================================================
    # CELL 7: Step 6 — Joining Tables (JOIN clause)
    # =========================================================================
    cells.append(make_markdown_cell([
        f"## Step 6: Joining Tables (JOIN clause)",
        f"",
        f"**📋 What you will do:**",
        f"Combine fields from two different tables. First, we will create an `owners` table, then join it with our `vehicles` table based on a shared identification key.",
        f"",
        f"**🔧 Code to type:**",
        f"```python",
        f"# Create the owners table",
        f"con.execute(\"\"\"",
        f"    CREATE TABLE owners (",
        f"        owner_id VARCHAR,",
        f"        owner_name VARCHAR,",
        f"        region VARCHAR",
        f"    )",
        f"\"\"\")",
        f"",
        f"# Populate the owners table",
        f"con.execute(\"\"\"",
        f"    INSERT INTO owners VALUES",
        f"    ('O001', 'Kofi Mensah', 'Greater Accra'),",
        f"    ('O002', 'Ama Serwaa', 'Ashanti'),",
        f"    ('O003', 'Kwame Osei', 'Western'),",
        f"    ('O004', 'Esi Boateng', 'Greater Accra')",
        f"\"\"\")",
        f"",
        f"# Join vehicles and owners on the shared owner_id",
        f"print('=== JOINED VEHICLES AND OWNERS ===')",
        f"con.sql(\"\"\"",
        f"    SELECT v.vehicle_id, v.make, v.model, o.owner_name, o.region",
        f"    FROM vehicles v",
        f"    INNER JOIN owners o ON v.owner_id = o.owner_id",
        f"\"\"\").show()",
        f"```",
        f"",
        f"**📖 Line-by-line explanation:**",
        f"- `FROM vehicles v`: Refers to the `vehicles` table, giving it a shorthand alias `v`.",
        f"- `INNER JOIN owners o ON v.owner_id = o.owner_id`: Matches rows in `vehicles` with rows in `owners` where the value in `owner_id` is identical. `o` is the alias for the `owners` table.",
        f"- `SELECT v.vehicle_id, ...`: Selects specific columns from each table using the table aliases to avoid ambiguity.",
        f"",
        f"**💡 Why this matters for DVLA:**",
        f"Data is often normalized (stored in separate tables) to reduce redundancy. In our main labs, we join vehicle registries with transaction logs using the unique registration ID to map payments to vehicles.",
    ]))
    cells.append(make_code_cell([
        f"# Step 6: Joining Tables",
        f"# Type your code below",
        f"",
    ]))

    # =========================================================================
    # CELL 8: Step 7 — Introduction to ETL using Pandas
    # =========================================================================
    cells.append(make_markdown_cell([
        f"## Step 7: Introduction to ETL (Extract, Transform, Load) using Pandas",
        f"",
        f"**📋 What you will do:**",
        f"Run a complete ETL pipeline programmatically using Python and **Pandas**:",
        f"1. **Extract**: Load raw vehicle data from a dictionary (simulating a CSV file download).",
        f"2. **Transform**: Clean up names, handle missing values, and calculate zonal regions.",
        f"3. **Load**: Save the clean dataset to a new CSV file inside your workspace.",
        f"",
        f"**🔧 Code to type:**",
        f"```python",
        f"# 1. EXTRACT: Create a raw DataFrame from simulated branch files",
        f"raw_data = {{",
        f"    'reg_no': ['GW-101-20', 'AS-502-18', 'WR-901-22', 'GW-303-21'],",
        f"    'owner': ['KOFI MENSAH', 'ama serwaa', 'KWAME OSEI', None],",
        f"    'fee_paid': [150.0, None, 200.0, -50.0]",
        f"}}",
        f"df = pd.DataFrame(raw_data)",
        f"print('--- RAW DATASET EXTRACTED ---')",
        f"print(df)",
        f"print()",
        f"",
        f"# 2. TRANSFORM: Clean and standardize the data",
        f"# A. Capitalize all owner names and replace missing names with 'Unknown'",
        f"df['owner'] = df['owner'].str.title().fillna('Unknown')",
        f"",
        f"# B. Fix fee anomalies: replace negative/null fees with a default fee of 100.0",
        f"df['fee_paid'] = df['fee_paid'].apply(lambda x: 100.0 if pd.isna(x) or x <= 0 else x)",
        f"",
        f"# C. Calculate Zonal Area Codes",
        f"def get_zonal_code(reg):",
        f"    if reg.startswith('GW'): return 'ACC-ZONE'",
        f"    elif reg.startswith('AS'): return 'ASH-ZONE'",
        f"    else: return 'WES-ZONE'",
        f"df['zonal_code'] = df['reg_no'].apply(get_zonal_code)",
        f"",
        f"print('--- DATASET TRANSFORMED ---')",
        f"print(df)",
        f"print()",
        f"",
        f"# 3. LOAD: Write clean data to your output folder",
        f"import os",
        f"os.makedirs('./output', exist_ok=True)",
        f"df.to_csv('./output/lab0_clean.csv', index=False)",
        f"print('✅ Saved clean file to ./output/lab0_clean.csv')",
        f"print('✅ ETL pipeline complete!')",
        f"```",
        f"",
        f"**📖 Line-by-line explanation:**",
        f"- `pd.DataFrame(raw_data)`: Converts a Python dictionary into a structured row-and-column DataFrame.",
        f"- `df['owner'].str.title()`: Standardizes the casing of string names (e.g. `KOFI MENSAH` and `ama serwaa` both become properly formatted title case `Kofi Mensah` and `Ama Serwaa`).",
        f"- `.fillna('Unknown')`: Finds any null/missing cells in the `owner` column and replaces them with the string `'Unknown'`.",
        f"- `df['fee_paid'].apply(...)`: Applies a lambda function to clean up fee records. If the fee is missing (`pd.isna(x)`) or invalid/negative (`x <= 0`), it defaults it to `100.0`.",
        f"- `df.to_csv(..., index=False)`: Writes the clean data to disk as a flat CSV file, excluding the row index column.",
        f"",
        f"**💡 Why this matters for DVLA:**",
        f"This mimics exactly what we do in Lab 2. In real scenarios, we read hundreds of thousands of dirty records from legacy servers, clean fee entries, map regional offices, and load the output as a CSV or Parquet file for dashboard consumption.",
        f"",
        f"---",
        f"*Lab 0 Complete — You have successfully learned the fundamentals of SQL and ETL! You are now fully prepared to tackle Lab 1.*",
    ]))
    cells.append(make_code_cell([
        f"# Step 7: Introduction to ETL",
        f"# Type your code below",
        f"",
    ]))

    # =========================================================================
    # CELL 9: Cleanup — Close connection
    # =========================================================================
    cells.append(make_markdown_cell([
        f"## Cleanup: Close the Connection",
        f"",
        f"**🔧 Code to type:**",
        f"```python",
        f"# Close database connections when finished",
        f"con.close()",
        f"print('✅ DuckDB connection closed.')",
        f"```",
    ]))
    cells.append(make_code_cell([
        f"# Cleanup: Close the connection",
        f"# Type your code below",
        f"",
    ]))

    return nb


# =============================================================================
# LAB 1: SQL PROFILING AND EXTRACTION (DuckDB)
# =============================================================================

def build_lab1(student_name: str, role: str, student_folder: str) -> dict:
    """
    Build Lab1_SQL_Profiling_and_Extraction.ipynb.

    This notebook guides students through profiling DVLA Ghana's legacy
    vehicle registration and payment data using DuckDB — an in-process
    SQL OLAP database engine. Students learn to identify data quality
    issues (duplicates, nulls, orphans, invalid amounts) using pure SQL.

    Parameters:
        student_name:   The student's display name for personalization.
        role:           The student's job role/title.
        student_folder: The student's workspace folder name.

    Returns:
        A complete notebook dictionary ready to be saved as .ipynb.
    """
    nb = create_notebook_skeleton()
    cells = nb["cells"]

    # =========================================================================
    # CELL 1: Welcome & Context
    # =========================================================================
    cells.append(make_markdown_cell([
        f"# 🏛️ Lab 1: SQL Data Profiling & Extraction",
        f"",
        f"**Welcome, {student_name}!** ({role})",
        f"",
        f"## Background",
        f"",
        f"The Driver and Vehicle Licensing Authority (DVLA) Ghana maintains a legacy vehicle registration ",
        f"database that has accumulated data quality issues over years of manual entry, system migrations, ",
        f"and inconsistent data capture across 20+ regional branch offices. Before any modernization or ",
        f"analytical reporting can be trusted, we must first **profile** this data to understand the scale ",
        f"and nature of the problems.",
        f"",
        f"## What You Will Learn",
        f"",
        f"In this lab, you will use **DuckDB** — a fast, in-process SQL database engine — to:",
        f"",
        f"1. Load raw CSV datasets into in-memory tables",
        f"2. Inspect table schemas and row counts",
        f"3. Identify exact duplicate records",
        f"4. Profile missing identification fields",
        f"5. Detect payment anomalies (zero/negative amounts)",
        f"6. Find orphan payment records with no matching vehicle registration",
        f"7. Summarize anomalies by regional branch office",
        f"",
        f"## Datasets",
        f"",
        f"| File | Description |",
        f"|---|---|",
        f"| `../raw_data/legacy_vehicle_registry.csv` | 50,000+ vehicle registration records |",
        f"| `../raw_data/payment_transaction_log.csv` | 50,000+ payment transaction records |",
        f"",
        f"---",
    ]))

    # =========================================================================
    # CELL 2: Step 1 — Install & Import DuckDB
    # =========================================================================
    cells.append(make_markdown_cell([
        f"## Step 1: Install and Import DuckDB",
        f"",
        f"**📋 What you will do:**",
        f"Install the DuckDB Python package (if not already installed) and import it.",
        f"",
        f"**🔧 Code to type:**",
        f"```python",
        f"# Install DuckDB if needed (only runs once)",
        f"!pip install duckdb --quiet",
        f"",
        f"# Import the DuckDB library",
        f"import duckdb",
        f"",
        f"print('DuckDB version:', duckdb.__version__)",
        f"print('✅ DuckDB ready!')",
        f"```",
        f"",
        f"**📖 Line-by-line explanation:**",
        f"- `!pip install duckdb --quiet`: The `!` prefix runs a shell command from inside Jupyter. ",
        f"  `--quiet` suppresses verbose output. This installs DuckDB if it's not already available.",
        f"- `import duckdb`: Loads the DuckDB library into your Python session. DuckDB is an ",
        f"  **in-process** database — unlike PostgreSQL or MySQL, it runs entirely inside your Python ",
        f"  process with zero external server setup.",
        f"- `duckdb.__version__`: Prints the installed version for debugging.",
        f"",
        f"**💡 Why this matters for DVLA:**",
        f"DuckDB can query CSV files directly without needing to set up a database server. This makes it ",
        f"ideal for quick data profiling in field offices where IT infrastructure may be limited.",
    ]))
    cells.append(make_code_cell([
        f"# Step 1: Install and Import DuckDB",
        f"# Type your code below",
        f"",
    ]))

    # =========================================================================
    # CELL 3: Step 2 — Create In-Memory Connection & Load CSVs
    # =========================================================================
    cells.append(make_markdown_cell([
        f"## Step 2: Create an In-Memory Connection and Load CSV Files",
        f"",
        f"**📋 What you will do:**",
        f"Create a DuckDB in-memory database connection and load both raw CSV files into tables.",
        f"",
        f"**🔧 Code to type:**",
        f"```python",
        f"# Create an in-memory DuckDB connection",
        f"con = duckdb.connect()",
        f"",
        f"# Load the vehicle registry CSV into a table called 'registry'",
        f"con.execute(\"\"\"",
        f"    CREATE TABLE registry AS",
        f"    SELECT * FROM read_csv_auto('../raw_data/legacy_vehicle_registry.csv')",
        f"\"\"\")",
        f"",
        f"# Load the payment transaction log CSV into a table called 'payments'",
        f"con.execute(\"\"\"",
        f"    CREATE TABLE payments AS",
        f"    SELECT * FROM read_csv_auto('../raw_data/payment_transaction_log.csv')",
        f"\"\"\")",
        f"",
        f"print('✅ Both tables loaded successfully!')",
        f"```",
        f"",
        f"**📖 Line-by-line explanation:**",
        f"- `duckdb.connect()`: Creates a new in-memory database. Data lives only in RAM — nothing ",
        f"  is written to disk. When you close the connection, the data is gone.",
        f"- `CREATE TABLE registry AS SELECT * FROM read_csv_auto(...)`: This is DuckDB's powerful ",
        f"  CSV reader. `read_csv_auto` automatically detects delimiters, data types, and headers. ",
        f"  The result is stored as a named table called `registry`.",
        f"- The path `../raw_data/` means 'go up one directory from this notebook, then into raw_data'. ",
        f"  This works because your notebook is inside your personal workspace folder (e.g., `./{student_folder}/`).",
        f"",
        f"**💡 Why this matters for DVLA:**",
        f"Loading data into memory tables allows us to run SQL queries at high speed without modifying ",
        f"the original CSV files. The raw data remains untouched — this is the principle of ",
        f"**non-destructive profiling**.",
    ]))
    cells.append(make_code_cell([
        f"# Step 2: Create In-Memory Connection and Load CSVs",
        f"# Type your code below",
        f"",
    ]))

    # =========================================================================
    # CELL 4: Step 3 — Inspect Table Schemas
    # =========================================================================
    cells.append(make_markdown_cell([
        f"## Step 3: Inspect Table Schemas",
        f"",
        f"**📋 What you will do:**",
        f"Examine the column names, data types, and nullability of both tables. This is always the ",
        f"first step in any data profiling exercise — you need to understand what you're working with.",
        f"",
        f"**🔧 Code to type:**",
        f"```python",
        f"# Inspect the vehicle registry table structure",
        f"print('=== VEHICLE REGISTRY SCHEMA ===')",
        f"con.sql('DESCRIBE registry').show()",
        f"",
        f"print()",
        f"",
        f"# Inspect the payment transactions table structure",
        f"print('=== PAYMENT TRANSACTIONS SCHEMA ===')",
        f"con.sql('DESCRIBE payments').show()",
        f"```",
        f"",
        f"**📖 Line-by-line explanation:**",
        f"- `DESCRIBE registry`: A SQL command that returns metadata about the table — column names, ",
        f"  data types (VARCHAR, DOUBLE, etc.), and whether nulls are allowed. DuckDB's `read_csv_auto` ",
        f"  inferred these types automatically.",
        f"- `.show()`: Prints the result in a formatted table directly in the Jupyter output cell.",
        f"",
        f"**💡 Why this matters for DVLA:**",
        f"Notice that `Registration_Date` may appear as VARCHAR (text) rather than DATE. This is because ",
        f"our raw data contains **mixed date formats** (YYYY-MM-DD and DD/MM/YYYY), so DuckDB cannot ",
        f"safely cast it to a date type. This is exactly the kind of issue we need to flag.",
    ]))
    cells.append(make_code_cell([
        f"# Step 3: Inspect Table Schemas",
        f"# Type your code below",
        f"",
    ]))

    # =========================================================================
    # CELL 5: Step 4 — Basic Profiling (Row Counts & Distinct Values)
    # =========================================================================
    cells.append(make_markdown_cell([
        f"## Step 4: Basic Profiling — Row Counts and Distinct Values",
        f"",
        f"**📋 What you will do:**",
        f"Count total rows and distinct values in key columns. This gives you a quick health check ",
        f"of the data — if total rows differ significantly from distinct rows, you have duplicates.",
        f"",
        f"**🔧 Code to type:**",
        f"```python",
        f"# Count total and distinct rows in the vehicle registry",
        f"con.sql(\"\"\"",
        f"    SELECT",
        f"        COUNT(*)                         AS total_rows,",
        f"        COUNT(DISTINCT Registration_ID)  AS unique_registrations,",
        f"        COUNT(DISTINCT Chassis_Number)    AS unique_chassis,",
        f"        COUNT(DISTINCT Owner_Name)        AS unique_owners,",
        f"        COUNT(DISTINCT Regional_Office)   AS branch_count",
        f"    FROM registry",
        f"\"\"\").show()",
        f"",
        f"# Count total and distinct rows in the payment log",
        f"con.sql(\"\"\"",
        f"    SELECT",
        f"        COUNT(*)                         AS total_rows,",
        f"        COUNT(DISTINCT Transaction_ID)   AS unique_transactions,",
        f"        COUNT(DISTINCT Registration_ID)  AS unique_linked_vehicles,",
        f"        COUNT(DISTINCT Payment_Channel)  AS channel_count",
        f"    FROM payments",
        f"\"\"\").show()",
        f"```",
        f"",
        f"**📖 Line-by-line explanation:**",
        f"- `COUNT(*)`: Counts every row in the table, including duplicates.",
        f"- `COUNT(DISTINCT column)`: Counts only unique values. If `COUNT(*)` is 52,500 but ",
        f"  `COUNT(DISTINCT Registration_ID)` is 50,000, there are approximately 2,500 duplicate rows.",
        f"- `AS alias`: Gives each result column a readable name.",
        f"",
        f"**💡 Why this matters for DVLA:**",
        f"If the total row count is significantly higher than the distinct registration count, ",
        f"it means the same vehicle may have been registered multiple times — inflating fleet ",
        f"statistics and potentially enabling double-billing.",
    ]))
    cells.append(make_code_cell([
        f"# Step 4: Basic Profiling",
        f"# Type your code below",
        f"",
    ]))

    # =========================================================================
    # CELL 6: Step 5 — Duplicate Detection
    # =========================================================================
    cells.append(make_markdown_cell([
        f"## Step 5: Identify Exact Duplicate Records",
        f"",
        f"**📋 What you will do:**",
        f"Find rows that appear more than once by grouping on all columns. The SQL `HAVING` clause ",
        f"filters groups to show only those with a count greater than 1.",
        f"",
        f"**🔧 Code to type:**",
        f"```python",
        f"# Find exact duplicate vehicle registration records",
        f"con.sql(\"\"\"",
        f"    SELECT",
        f"        Registration_ID,",
        f"        Chassis_Number,",
        f"        Owner_Name,",
        f"        Regional_Office,",
        f"        COUNT(*) AS occurrence_count",
        f"    FROM registry",
        f"    GROUP BY Registration_ID, Chassis_Number, Owner_Name, Regional_Office",
        f"    HAVING COUNT(*) > 1",
        f"    ORDER BY occurrence_count DESC",
        f"    LIMIT 20",
        f"\"\"\").show()",
        f"```",
        f"",
        f"**📖 Line-by-line explanation:**",
        f"- `GROUP BY col1, col2, ...`: Groups all rows that have identical values across the listed ",
        f"  columns into a single bucket.",
        f"- `HAVING COUNT(*) > 1`: The `HAVING` clause is like `WHERE`, but it filters **after** grouping. ",
        f"  It keeps only groups where the count exceeds 1 — i.e., duplicates.",
        f"- `ORDER BY occurrence_count DESC`: Shows the most-duplicated records first.",
        f"- `LIMIT 20`: Restricts output to the top 20 for readability.",
        f"",
        f"**💡 Why this matters for DVLA:**",
        f"Duplicate registrations can occur when the same vehicle is processed at multiple branch ",
        f"offices, or when paper records are digitized more than once. Each duplicate inflates the ",
        f"fleet count and could result in duplicate fee collections — a revenue integrity issue.",
    ]))
    cells.append(make_code_cell([
        f"# Step 5: Duplicate Detection",
        f"# Type your code below",
        f"",
    ]))

    # =========================================================================
    # CELL 7: Step 6 — Null National ID Profiling
    # =========================================================================
    cells.append(make_markdown_cell([
        f"## Step 6: Profile Missing National ID Numbers",
        f"",
        f"**📋 What you will do:**",
        f"Count how many vehicle registrations have a missing (NULL) Ghana Card number, broken down ",
        f"by regional branch office. This reveals which offices have the worst data capture practices.",
        f"",
        f"**🔧 Code to type:**",
        f"```python",
        f"# Count null National_ID_Number by regional office",
        f"con.sql(\"\"\"",
        f"    SELECT",
        f"        Regional_Office,",
        f"        COUNT(*)                                              AS total_records,",
        f"        SUM(CASE WHEN National_ID_Number IS NULL THEN 1 ELSE 0 END) AS null_id_count,",
        f"        ROUND(SUM(CASE WHEN National_ID_Number IS NULL THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS null_percentage",
        f"    FROM registry",
        f"    GROUP BY Regional_Office",
        f"    ORDER BY null_percentage DESC",
        f"\"\"\").show()",
        f"```",
        f"",
        f"**📖 Line-by-line explanation:**",
        f"- `SUM(CASE WHEN ... THEN 1 ELSE 0 END)`: This is a conditional count. For each row, if ",
        f"  `National_ID_Number IS NULL`, it adds 1; otherwise 0. The SUM gives the total null count.",
        f"- `ROUND(... * 100.0 / COUNT(*), 2)`: Calculates the percentage of null IDs and rounds to ",
        f"  2 decimal places. The `100.0` (not `100`) forces floating-point division.",
        f"- `ORDER BY null_percentage DESC`: Shows the offices with the highest null rates first.",
        f"",
        f"**💡 Why this matters for DVLA:**",
        f"A vehicle registration without a verified National ID means the owner cannot be definitively ",
        f"identified. This creates risks for law enforcement (stolen vehicles), insurance claims, ",
        f"and tax collection. The Ghana Card integration initiative aims to close this gap.",
    ]))
    cells.append(make_code_cell([
        f"# Step 6: Null National ID Profiling",
        f"# Type your code below",
        f"",
    ]))

    # =========================================================================
    # CELL 8: Step 7 — Payment Anomalies (Zero/Negative Amounts)
    # =========================================================================
    cells.append(make_markdown_cell([
        f"## Step 7: Detect Payment Anomalies — Zero and Negative Amounts",
        f"",
        f"**📋 What you will do:**",
        f"Identify payment transactions where the amount paid is zero or negative. These represent ",
        f"potential revenue leakage — money that should have been collected but wasn't.",
        f"",
        f"**🔧 Code to type:**",
        f"```python",
        f"# Find payments with zero or negative amounts",
        f"con.sql(\"\"\"",
        f"    SELECT",
        f"        Transaction_ID,",
        f"        Registration_ID,",
        f"        Amount_Paid_GHS,",
        f"        Payment_Channel,",
        f"        Payment_Timestamp",
        f"    FROM payments",
        f"    WHERE Amount_Paid_GHS <= 0",
        f"    ORDER BY Amount_Paid_GHS ASC",
        f"    LIMIT 20",
        f"\"\"\").show()",
        f"",
        f"# Count total anomalous payments",
        f"con.sql(\"\"\"",
        f"    SELECT",
        f"        COUNT(*) AS total_anomalous_payments,",
        f"        SUM(Amount_Paid_GHS) AS total_revenue_loss_ghs",
        f"    FROM payments",
        f"    WHERE Amount_Paid_GHS <= 0",
        f"\"\"\").show()",
        f"```",
        f"",
        f"**📖 Line-by-line explanation:**",
        f"- `WHERE Amount_Paid_GHS <= 0`: Filters for payments that are zero (no payment received) ",
        f"  or negative (potentially fraudulent refund entries).",
        f"- `ORDER BY Amount_Paid_GHS ASC`: Shows the most negative (largest loss) values first.",
        f"- `SUM(Amount_Paid_GHS)`: When summing negative values, the total represents the ",
        f"  aggregate revenue loss. A large negative total is a red flag for the finance team.",
        f"",
        f"**💡 Why this matters for DVLA:**",
        f"Zero-amount payments may indicate processing errors at POS terminals. Negative amounts ",
        f"could indicate unauthorized refunds. Both must be investigated by the Revenue Assurance unit.",
    ]))
    cells.append(make_code_cell([
        f"# Step 7: Payment Anomalies",
        f"# Type your code below",
        f"",
    ]))

    # =========================================================================
    # CELL 9: Step 8 — Orphan Payment Detection
    # =========================================================================
    cells.append(make_markdown_cell([
        f"## Step 8: Detect Orphan Payments — Unlinked Registration IDs",
        f"",
        f"**📋 What you will do:**",
        f"Find payment transactions that reference a Registration_ID which does not exist in the ",
        f"vehicle registry. These 'orphan' payments represent money collected for vehicles that have ",
        f"no official registration record.",
        f"",
        f"**🔧 Code to type:**",
        f"```python",
        f"# Find payments with no matching vehicle registration",
        f"con.sql(\"\"\"",
        f"    SELECT",
        f"        p.Transaction_ID,",
        f"        p.Registration_ID,",
        f"        p.Amount_Paid_GHS,",
        f"        p.Payment_Channel",
        f"    FROM payments p",
        f"    LEFT JOIN registry r ON p.Registration_ID = r.Registration_ID",
        f"    WHERE r.Registration_ID IS NULL",
        f"    LIMIT 20",
        f"\"\"\").show()",
        f"",
        f"# Count total orphan payments and their financial impact",
        f"con.sql(\"\"\"",
        f"    SELECT",
        f"        COUNT(*)                 AS orphan_payment_count,",
        f"        ROUND(SUM(p.Amount_Paid_GHS), 2)  AS orphan_revenue_ghs",
        f"    FROM payments p",
        f"    LEFT JOIN registry r ON p.Registration_ID = r.Registration_ID",
        f"    WHERE r.Registration_ID IS NULL",
        f"\"\"\").show()",
        f"```",
        f"",
        f"**📖 Line-by-line explanation:**",
        f"- `LEFT JOIN registry r ON p.Registration_ID = r.Registration_ID`: A LEFT JOIN returns all ",
        f"  rows from the left table (payments) and matching rows from the right table (registry). ",
        f"  If there's no match, the right-side columns are NULL.",
        f"- `WHERE r.Registration_ID IS NULL`: Filters for payments where no matching registration ",
        f"  was found — these are the orphan records.",
        f"- Table aliases (`p` for payments, `r` for registry) make the query more readable.",
        f"",
        f"**💡 Why this matters for DVLA:**",
        f"Orphan payments could indicate: (a) vehicles registered under a different ID format, ",
        f"(b) payments processed at unauthorized collection points, or (c) data migration errors ",
        f"where the registry record was lost. Each scenario requires different remediation.",
    ]))
    cells.append(make_code_cell([
        f"# Step 8: Orphan Payment Detection",
        f"# Type your code below",
        f"",
    ]))

    # =========================================================================
    # CELL 10: Step 9 — Summary by Regional Office
    # =========================================================================
    cells.append(make_markdown_cell([
        f"## Step 9: Anomaly Summary by Regional Office",
        f"",
        f"**📋 What you will do:**",
        f"Create a comprehensive summary showing all data quality issues aggregated by regional branch ",
        f"office. This gives DVLA leadership a clear picture of which offices need the most attention.",
        f"",
        f"**🔧 Code to type:**",
        f"```python",
        f"# Comprehensive anomaly summary per regional office",
        f"con.sql(\"\"\"",
        f"    SELECT",
        f"        r.Regional_Office,",
        f"        COUNT(DISTINCT r.Registration_ID) AS unique_vehicles,",
        f"        SUM(CASE WHEN r.National_ID_Number IS NULL THEN 1 ELSE 0 END) AS missing_ids,",
        f"        COUNT(*) - COUNT(DISTINCT r.Registration_ID || r.Chassis_Number || COALESCE(r.Owner_Name, '')) AS approx_duplicates",
        f"    FROM registry r",
        f"    GROUP BY r.Regional_Office",
        f"    ORDER BY missing_ids DESC",
        f"\"\"\").show()",
        f"```",
        f"",
        f"**📖 Line-by-line explanation:**",
        f"- `COUNT(DISTINCT r.Registration_ID)`: Counts unique vehicles per office.",
        f"- `SUM(CASE WHEN ... IS NULL ...)`: Counts missing National IDs per office.",
        f"- `COALESCE(r.Owner_Name, '')`: Replaces NULL owner names with empty string for concatenation.",
        f"- The difference between total count and distinct concatenated keys approximates duplicates.",
        f"",
        f"**💡 Why this matters for DVLA:**",
        f"This summary becomes the basis for the **Data Cleanup Initiative** action plan — offices ",
        f"with the highest anomaly rates should be prioritized for staff retraining and system audits.",
    ]))
    cells.append(make_code_cell([
        f"# Step 9: Anomaly Summary by Regional Office",
        f"# Type your code below",
        f"",
    ]))

    # =========================================================================
    # CELL 11: Step 10 — Payment Channel Distribution
    # =========================================================================
    cells.append(make_markdown_cell([
        f"## Step 10: Payment Channel Distribution Analysis",
        f"",
        f"**📋 What you will do:**",
        f"Analyze how payments are distributed across different channels (MTN MoMo, Bank Branch, etc.) ",
        f"and identify which channels have the highest rates of anomalous transactions.",
        f"",
        f"**🔧 Code to type:**",
        f"```python",
        f"# Payment channel distribution with anomaly rates",
        f"con.sql(\"\"\"",
        f"    SELECT",
        f"        Payment_Channel,",
        f"        COUNT(*)                                         AS total_transactions,",
        f"        ROUND(SUM(CASE WHEN Amount_Paid_GHS > 0 THEN Amount_Paid_GHS ELSE 0 END), 2) AS valid_revenue_ghs,",
        f"        SUM(CASE WHEN Amount_Paid_GHS <= 0 THEN 1 ELSE 0 END)    AS anomalous_count,",
        f"        ROUND(SUM(CASE WHEN Amount_Paid_GHS <= 0 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS anomaly_rate_pct",
        f"    FROM payments",
        f"    GROUP BY Payment_Channel",
        f"    ORDER BY total_transactions DESC",
        f"\"\"\").show()",
        f"```",
        f"",
        f"**📖 Line-by-line explanation:**",
        f"- `SUM(CASE WHEN Amount_Paid_GHS > 0 THEN Amount_Paid_GHS ELSE 0 END)`: Sums only valid ",
        f"  (positive) payments, ignoring zero and negative entries.",
        f"- `anomaly_rate_pct`: Shows the percentage of anomalous transactions per channel. A high ",
        f"  rate on a specific channel may indicate a systemic issue with that payment gateway.",
        f"",
        f"**💡 Why this matters for DVLA:**",
        f"If MTN MoMo shows a disproportionately high anomaly rate compared to Bank Branch, it could ",
        f"indicate integration issues with the mobile money gateway that need to be escalated to the ",
        f"payment service provider.",
    ]))
    cells.append(make_code_cell([
        f"# Step 10: Payment Channel Distribution",
        f"# Type your code below",
        f"",
    ]))

    # =========================================================================
    # CELL 12: Step 11 — Discussion & Next Steps
    # =========================================================================
    cells.append(make_markdown_cell([
        f"## Step 11: Discussion — What Do These Findings Mean?",
        f"",
        f"### Key Findings from Our Profiling",
        f"",
        f"After completing the analysis above, you should have identified:",
        f"",
        f"| Issue | Expected Scale | Impact |",
        f"|---|---|---|",
        f"| Duplicate registrations | ~5% of records | Inflated fleet statistics, double billing |",
        f"| Missing National IDs | ~10% of records | Unverifiable vehicle ownership |",
        f"| Mixed date formats | ~30% of records | Breaks automated date-based reporting |",
        f"| Zero/negative payments | ~5% of transactions | Direct revenue leakage |",
        f"| Orphan payments | ~10% of transactions | Unlinked revenue, potential fraud |",
        f"",
        f"### What Happens Next?",
        f"",
        f"In **Lab 2**, you will use **Apache PySpark** to:",
        f"",
        f"1. **Clean** these issues programmatically at scale",
        f"2. **Standardize** date formats across all records",
        f"3. **Map** regional offices to the new 2026 Zonal Area Codes",
        f"4. **Extract** the latest payment record per vehicle",
        f"5. **Export** clean data for Power BI dashboard reporting",
        f"",
        f"### 🎓 Reflection Questions",
        f"",
        f"1. Which regional office has the worst data quality? What might explain this?",
        f"2. What is the total revenue at risk from zero/negative payments?",
        f"3. How would you prioritize the cleanup — fix duplicates first, or missing IDs?",
        f"",
        f"---",
        f"*Lab 1 Complete — {student_name}, proceed to Lab 2 when ready.*",
    ]))

    # =========================================================================
    # CELL 13: Cleanup
    # =========================================================================
    cells.append(make_markdown_cell([
        f"## Cleanup: Close the DuckDB Connection",
        f"",
        f"**🔧 Code to type:**",
        f"```python",
        f"# Always close database connections when finished",
        f"con.close()",
        f"print('✅ DuckDB connection closed.')",
        f"```",
        f"",
        f"**📖 Explanation:**",
        f"Closing the connection releases the in-memory tables and frees RAM. This is good practice, ",
        f"especially on a shared server where multiple students are working simultaneously.",
    ]))
    cells.append(make_code_cell([
        f"# Cleanup: Close the DuckDB Connection",
        f"# Type your code below",
        f"",
    ]))

    return nb


# =============================================================================
# LAB 2: PySpark ETL AND TRANSFORMATION
# =============================================================================

def build_lab2(student_name: str, role: str) -> dict:
    """
    Build Lab2_PySpark_ETL_and_Transformation.ipynb.

    This notebook guides students through a full ETL pipeline using Apache
    PySpark: deduplication, null handling, date standardization, broadcast
    joins for zonal code mapping, window functions for latest-record
    extraction, and final export to Parquet and CSV.

    Parameters:
        student_name: The student's display name for personalization.
        role:         The student's job role/title.

    Returns:
        A complete notebook dictionary ready to be saved as .ipynb.
    """
    nb = create_notebook_skeleton()
    cells = nb["cells"]

    # =========================================================================
    # CELL 1: Welcome & Spark Architecture
    # =========================================================================
    cells.append(make_markdown_cell([
        f"# ⚡ Lab 2: PySpark ETL & Transformation Pipeline",
        f"",
        f"**Welcome back, {student_name}!** ({role})",
        f"",
        f"## Background",
        f"",
        f"In Lab 1, you profiled DVLA Ghana's legacy data and identified critical quality issues: ",
        f"duplicates, missing IDs, mixed date formats, orphan payments, and revenue leakage. Now it's ",
        f"time to **fix** these issues using a scalable ETL (Extract, Transform, Load) pipeline.",
        f"",
        f"## What is Apache Spark?",
        f"",
        f"Apache Spark is a **distributed data processing engine** designed to handle massive datasets ",
        f"across clusters of machines. Even when running locally (as we do in this lab), Spark provides:",
        f"",
        f"- **Lazy evaluation**: Spark builds a plan (DAG — Directed Acyclic Graph) of transformations ",
        f"  but doesn't execute them until you request an action (like `.count()` or `.show()`). This ",
        f"  allows Spark to optimize the execution plan.",
        f"- **In-memory processing**: Data is kept in RAM between transformations, avoiding slow disk I/O.",
        f"- **Fault tolerance**: If a computation fails, Spark can recompute it from the original data.",
        f"",
        f"## Memory Configuration",
        f"",
        f"> ⚠️ **Important**: We limit Spark's driver memory to **2GB** (`spark.driver.memory = \"2g\"`) ",
        f"> because multiple students are running Spark sessions concurrently on this server. Using more ",
        f"> memory could cause an Out-of-Memory (OOM) kernel panic that crashes the entire server.",
        f"",
        f"## What You Will Build",
        f"",
        f"| Step | Transformation | Purpose |",
        f"|---|---|---|",
        f"| 1 | Deduplication | Remove exact duplicate records |",
        f"| 2 | Null handling | Flag unverified vehicle owners |",
        f"| 3 | Date standardization | Unify to YYYY-MM-DD format |",
        f"| 4 | Broadcast join | Map offices to 2026 Zonal Area Codes |",
        f"| 5 | Window function | Extract latest payment per vehicle |",
        f"| 6 | Revenue flagging | Tag anomalous transactions |",
        f"| 7 | Export | Save as Parquet + flat CSV for Power BI |",
        f"",
        f"---",
    ]))

    # =========================================================================
    # CELL 2: Step 1 — Import Libraries & Create SparkSession
    # =========================================================================
    cells.append(make_markdown_cell([
        f"## Step 1: Import Libraries and Create a SparkSession",
        f"",
        f"**📋 What you will do:**",
        f"Import the PySpark libraries and create a local SparkSession — the entry point to all ",
        f"Spark functionality.",
        f"",
        f"**🔧 Code to type:**",
        f"```python",
        f"# Import PySpark modules",
        f"from pyspark.sql import SparkSession",
        f"from pyspark.sql import functions as F",
        f"from pyspark.sql.window import Window",
        f"from pyspark.sql.types import StructType, StructField, StringType",
        f"import os",
        f"",
        f"# Create a local SparkSession with a 2GB memory cap",
        f"spark = SparkSession.builder \\",
        f"    .appName('DVLA_ETL_{student_name.replace(' ', '_')}') \\",
        f"    .master('local[*]') \\",
        f"    .config('spark.driver.memory', '2g') \\",
        f"    .config('spark.sql.shuffle.partitions', '8') \\",
        f"    .config('spark.sql.legacy.timeParserPolicy', 'LEGACY') \\",
        f"    .config('spark.ui.showConsoleProgress', 'false') \\",
        f"    .getOrCreate()",
        f"",
        f"# Reduce Spark's verbose logging",
        f"spark.sparkContext.setLogLevel('WARN')",
        f"",
        f"print(f'Spark version: {{spark.version}}')",
        f"print(f'App name: {{spark.sparkContext.appName}}')",
        f"print('✅ SparkSession created successfully!')",
        f"```",
        f"",
        f"**📖 Line-by-line explanation:**",
        f"- `SparkSession.builder`: Starts the builder pattern to configure Spark.",
        f"- `.appName(...)`: Names your Spark application — visible in the Spark UI for monitoring.",
        f"- `.master('local[*]')`: Runs Spark locally using all available CPU cores (`*`). In a ",
        f"  production cluster, this would be `yarn` or `mesos`.",
        f"- `.config('spark.driver.memory', '2g')`: Limits the JVM heap to 2GB. The driver is the ",
        f"  process that coordinates your Spark program.",
        f"- `.config('spark.sql.shuffle.partitions', '8')`: Reduces the default 200 shuffle partitions ",
        f"  to 8, which is more appropriate for our dataset size (~50K rows).",
        f"- `.config('spark.sql.legacy.timeParserPolicy', 'LEGACY')`: Reverts the datetime parsing ",
        f"  behavior to legacy mode, which safely returns NULL on pattern mismatches instead of raising exceptions.",
        f"- `.getOrCreate()`: Creates a new session or reuses an existing one.",
        f"",
        f"**⚠️ Notes on Common Startup Warnings:**",
        f"When running this cell, you will see a few warning lines printed by Java in the console output. ",
        f"**These are completely normal, harmless, and expected in any local development environment:**",
        f"- `WARNING: Using incubator modules: jdk.incubator.vector`: Java 17+ prints this when Spark ",
        f"  activates CPU vector math optimizations for faster calculations.",
        f"- `WARN NativeCodeLoader: Unable to load native-hadoop library...`: Occurs because the system ",
        f"  uses Spark's built-in Java file reader instead of Hadoop's compiled native C libraries. This has ",
        f"  zero impact on local file processing.",
        f"- `Using Spark's default log4j profile...`: General setup info logged before your custom ",
        f"  log level (`WARN`) takes effect.",
        f"",
        f"**💡 Why this matters for DVLA:**",
        f"In a production environment, DVLA could run this same code on a Spark cluster (e.g., AWS EMR ",
        f"or Azure HDInsight) to process millions of records. The code structure remains identical — only ",
        f"the `.master()` configuration changes.",
    ]))
    cells.append(make_code_cell([
        f"# Step 1: Import Libraries and Create SparkSession",
        f"# Type your code below",
        f"",
    ]))

    # =========================================================================
    # CELL 3: Step 2 — Load CSV Files
    # =========================================================================
    cells.append(make_markdown_cell([
        f"## Step 2: Load the Raw CSV Datasets",
        f"",
        f"**📋 What you will do:**",
        f"Read both CSV files from the shared `raw_data` directory into Spark DataFrames.",
        f"",
        f"**🔧 Code to type:**",
        f"```python",
        f"# Load the vehicle registry",
        f"registry_df = spark.read.csv(",
        f"    '../raw_data/legacy_vehicle_registry.csv',",
        f"    header=True,",
        f"    inferSchema=True",
        f")",
        f"",
        f"# Load the payment transactions",
        f"payments_df = spark.read.csv(",
        f"    '../raw_data/payment_transaction_log.csv',",
        f"    header=True,",
        f"    inferSchema=True",
        f")",
        f"",
        f"print(f'Registry rows: {{registry_df.count():,}}')",
        f"print(f'Payment rows:  {{payments_df.count():,}}')",
        f"print()",
        f"registry_df.printSchema()",
        f"```",
        f"",
        f"**📖 Line-by-line explanation:**",
        f"- `spark.read.csv(path, header=True, inferSchema=True)`: Reads a CSV file into a Spark ",
        f"  DataFrame. `header=True` tells Spark the first row contains column names. `inferSchema=True` ",
        f"  asks Spark to automatically detect data types (string, integer, double, etc.).",
        f"- `.count()`: An **action** that triggers actual computation. Spark reads the entire file and ",
        f"  counts the rows. This is when lazy evaluation ends and real processing begins.",
        f"- `.printSchema()`: Displays the column names, data types, and nullability.",
        f"",
        f"**💡 Why this matters for DVLA:**",
        f"Note that `Registration_Date` will be inferred as `string` (not date) because of the mixed ",
        f"formats. Spark cannot auto-detect dates when multiple formats coexist — we'll fix this in Step 5.",
    ]))
    cells.append(make_code_cell([
        f"# Step 2: Load Raw CSV Datasets",
        f"# Type your code below",
        f"",
    ]))

    # =========================================================================
    # CELL 4: Step 3 — Deduplication
    # =========================================================================
    cells.append(make_markdown_cell([
        f"## Step 3: Remove Duplicate Records",
        f"",
        f"**📋 What you will do:**",
        f"Remove exact duplicate rows from both datasets using Spark's `dropDuplicates()` method.",
        f"",
        f"**🔧 Code to type:**",
        f"```python",
        f"# Count before deduplication",
        f"reg_before = registry_df.count()",
        f"pay_before = payments_df.count()",
        f"",
        f"# Remove exact duplicate rows",
        f"registry_df = registry_df.dropDuplicates()",
        f"payments_df = payments_df.dropDuplicates()",
        f"",
        f"# Count after deduplication",
        f"reg_after = registry_df.count()",
        f"pay_after = payments_df.count()",
        f"",
        f"print(f'Registry: {{reg_before:,}} → {{reg_after:,}} (removed {{reg_before - reg_after:,}} duplicates)')",
        f"print(f'Payments: {{pay_before:,}} → {{pay_after:,}} (removed {{pay_before - pay_after:,}} duplicates)')",
        f"```",
        f"",
        f"**📖 Line-by-line explanation:**",
        f"- `dropDuplicates()`: Removes rows that are identical across ALL columns. Spark internally ",
        f"  performs a **shuffle** — redistributing data across partitions — to compare rows. This is ",
        f"  one of the most expensive operations in Spark.",
        f"- We count before and after to quantify the cleanup impact. This metric goes into our ",
        f"  dashboard's \"Data Cleansing & Quality Audit\" view.",
        f"",
        f"**💡 Why this matters for DVLA:**",
        f"Deduplication is the first step in any data cleanup. If we skip this, all downstream counts ",
        f"(vehicle fleet size, revenue totals) will be inflated by ~5%.",
    ]))
    cells.append(make_code_cell([
        f"# Step 3: Remove Duplicate Records",
        f"# Type your code below",
        f"",
    ]))

    # =========================================================================
    # CELL 5: Step 4 — Handle Null National IDs
    # =========================================================================
    cells.append(make_markdown_cell([
        f"## Step 4: Handle Missing National ID Numbers",
        f"",
        f"**📋 What you will do:**",
        f"Replace null (missing) `National_ID_Number` values with the placeholder `'UNVERIFIED_HOLDER'` ",
        f"and add a new column `Identity_Status` that flags each record as `VERIFIED` or `UNVERIFIED_HOLDER`.",
        f"",
        f"**🔧 Code to type:**",
        f"```python",
        f"# Add Identity_Status column based on whether National_ID is present",
        f"registry_df = registry_df.withColumn(",
        f"    'Identity_Status',",
        f"    F.when(F.col('National_ID_Number').isNull(), 'UNVERIFIED_HOLDER')",
        f"     .otherwise('VERIFIED')",
        f")",
        f"",
        f"# Replace null National_ID_Number with placeholder text",
        f"registry_df = registry_df.fillna({{'National_ID_Number': 'UNVERIFIED_HOLDER'}})",
        f"",
        f"# Verify: count by identity status",
        f"registry_df.groupBy('Identity_Status').count().show()",
        f"```",
        f"",
        f"**📖 Line-by-line explanation:**",
        f"- `F.when(condition, value).otherwise(value)`: PySpark's equivalent of SQL's CASE WHEN. ",
        f"  Creates a new column based on conditional logic.",
        f"- `F.col('National_ID_Number').isNull()`: Checks if the column value is NULL (missing).",
        f"- `.fillna({{'National_ID_Number': 'UNVERIFIED_HOLDER'}})`: Replaces all NULL values in the ",
        f"  specified column with the string 'UNVERIFIED_HOLDER'. We do this AFTER creating the status ",
        f"  column so the flag is set correctly.",
        f"- `.groupBy('Identity_Status').count()`: Quick verification — shows how many records are ",
        f"  VERIFIED vs UNVERIFIED_HOLDER.",
        f"",
        f"**💡 Why this matters for DVLA:**",
        f"Rather than deleting records with missing IDs (which would lose vehicle data), we flag them. ",
        f"This preserves the data while clearly marking which records need follow-up verification ",
        f"through the Ghana Card integration process.",
    ]))
    cells.append(make_code_cell([
        f"# Step 4: Handle Missing National IDs",
        f"# Type your code below",
        f"",
    ]))

    # =========================================================================
    # CELL 6: Step 5 — Standardize Date Formats
    # =========================================================================
    cells.append(make_markdown_cell([
        f"## Step 5: Standardize Date Formats",
        f"",
        f"**📋 What you will do:**",
        f"Convert all `Registration_Date` values to a uniform `YYYY-MM-DD` format. The raw data mixes ",
        f"two formats: `YYYY-MM-DD` (modern) and `DD/MM/YYYY` (legacy). We use PySpark's `coalesce()` ",
        f"to try parsing with both patterns.",
        f"",
        f"**🔧 Code to type:**",
        f"```python",
        f"# Try parsing as YYYY-MM-DD first, then as DD/MM/YYYY using try_to_date to return NULL on mismatch",
        f"registry_df = registry_df.withColumn(",
        f"    'Registration_Date',",
        f"    F.coalesce(",
        f"        F.try_to_date(F.col('Registration_Date'), 'yyyy-MM-dd'),",
        f"        F.try_to_date(F.col('Registration_Date'), 'dd/MM/yyyy')",
        f"    )",
        f")",
        f"",
        f"# Verify: check for any remaining null dates (would indicate unparseable formats)",
        f"null_dates = registry_df.filter(F.col('Registration_Date').isNull()).count()",
        f"print(f'Unparseable dates remaining: {{null_dates}}')",
        f"",
        f"# Show sample of standardized dates",
        f"registry_df.select('Registration_ID', 'Registration_Date').show(5)",
        f"```",
        f"",
        f"**📖 Line-by-line explanation:**",
        f"- `F.try_to_date(col, format)`: Attempts to parse a string column into a date using the ",
        f"  specified format pattern. Returns NULL if the string doesn't match the pattern, safely avoiding exceptions.",
        f"- `F.coalesce(expr1, expr2)`: Returns the first non-NULL expression. So if the date ",
        f"  parses as `yyyy-MM-dd`, use that result. If it returns NULL (wrong format), try ",
        f"  `dd/MM/yyyy` instead.",
        f"- This two-pass approach handles both formats without any data loss.",
        f"",
        f"**💡 Why this matters for DVLA:**",
        f"Standardized dates are essential for time-based reporting (e.g., 'How many vehicles were ",
        f"registered in Q1 2024?'). Mixed formats make such queries impossible without preprocessing.",
    ]))
    cells.append(make_code_cell([
        f"# Step 5: Standardize Date Formats",
        f"# Type your code below",
        f"",
    ]))

    # =========================================================================
    # CELL 7: Step 6 — Define Zonal Area Code Dictionary
    # =========================================================================
    cells.append(make_markdown_cell([
        f"## Step 6: Define the 2026 Zonal Area Code Dictionary",
        f"",
        f"**📋 What you will do:**",
        f"Create a small lookup table that maps each DVLA regional office to its new 2026 Zonal Area ",
        f"Code. This dictionary will be used in a broadcast join in the next step.",
        f"",
        f"**🔧 Code to type:**",
        f"```python",
        f"# Define the 2026 Zonal Area Code mapping",
        f"# Each regional office maps to a zone code and description",
        f"zonal_mapping = [",
        f"    ('Accra Metro', 'ACC-Z1', 'Central Accra'),",
        f"    ('Weija',       'ACC-Z2', 'West Accra'),",
        f"    ('Madina',      'ACC-Z3', 'East Accra'),",
        f"    ('Tema',        'ACC-Z4', 'Tema Industrial'),",
        f"    ('Kumasi',      'ASH-Z1', 'Kumasi Metro'),",
        f"    ('Obuasi',      'ASH-Z2', 'Ashanti South'),",
        f"    ('Mampong',     'ASH-Z2', 'Ashanti North'),",
        f"    ('Tamale',      'NOR-Z1', 'Northern Metro'),",
        f"    ('Takoradi',    'WES-Z1', 'Sekondi-Takoradi'),",
        f"    ('Tarkwa',      'WES-Z1', 'Western Mining Belt'),",
        f"    ('Cape Coast',  'CEN-Z1', 'Central Metro'),",
        f"    ('Winneba',     'CEN-Z1', 'Central Coast'),",
        f"    ('Koforidua',   'EAS-Z1', 'Eastern Metro'),",
        f"    ('Nkawkaw',     'EAS-Z1', 'Eastern Highlands'),",
        f"    ('Sunyani',     'BON-Z1', 'Bono Metro'),",
        f"    ('Techiman',    'BON-Z1', 'Bono East'),",
        f"    ('Bolgatanga',  'UPE-Z1', 'Upper East Metro'),",
        f"    ('Wa',          'UPW-Z1', 'Upper West Metro'),",
        f"    ('Ho',          'VOL-Z1', 'Volta Metro'),",
        f"    ('Aflao',       'VOL-Z1', 'Volta Border'),",
        f"]",
        f"",
        f"# Create a Spark DataFrame from the mapping",
        f"zonal_schema = StructType([",
        f"    StructField('Regional_Office', StringType(), False),",
        f"    StructField('Zonal_Area_Code', StringType(), False),",
        f"    StructField('Zone_Description', StringType(), False),",
        f"])",
        f"",
        f"zonal_df = spark.createDataFrame(zonal_mapping, schema=zonal_schema)",
        f"zonal_df.show(truncate=False)",
        f"print(f'Zonal mapping entries: {{zonal_df.count()}}')",
        f"```",
        f"",
        f"**📖 Line-by-line explanation:**",
        f"- `zonal_mapping`: A Python list of tuples. Each tuple contains three values: the current ",
        f"  Regional_Office name, the new Zonal_Area_Code, and a human-readable Zone_Description.",
        f"- `StructType([...])`: Explicitly defines the schema instead of relying on inference. This is ",
        f"  best practice for small lookup tables where you want guaranteed data types.",
        f"- `spark.createDataFrame(data, schema)`: Converts a Python list into a Spark DataFrame.",
        f"",
        f"**💡 Why this matters for DVLA:**",
        f"The 2026 Zonal Area Code harmonization is a real policy initiative to reorganize DVLA's ",
        f"administrative boundaries. This mapping ensures all vehicle records can be classified under ",
        f"the new zonal structure for decentralized reporting.",
    ]))
    cells.append(make_code_cell([
        f"# Step 6: Define Zonal Area Code Dictionary",
        f"# Type your code below",
        f"",
    ]))

    # =========================================================================
    # CELL 8: Step 7 — Broadcast Join
    # =========================================================================
    cells.append(make_markdown_cell([
        f"## Step 7: Broadcast Join — Map Offices to Zonal Codes",
        f"",
        f"**📋 What you will do:**",
        f"Join the vehicle registry with the Zonal Area Code dictionary using a **broadcast join**. ",
        f"This is a high-performance technique for joining a large table with a small lookup table.",
        f"",
        f"**🔧 Code to type:**",
        f"```python",
        f"from pyspark.sql.functions import broadcast",
        f"",
        f"# Perform a broadcast join",
        f"# The small zonal_df is broadcast (copied) to every executor node",
        f"registry_df = registry_df.join(",
        f"    broadcast(zonal_df),",
        f"    on='Regional_Office',",
        f"    how='left'",
        f")",
        f"",
        f"# Verify: check for unmatched offices (should be 0 if mapping is complete)",
        f"unmatched = registry_df.filter(F.col('Zonal_Area_Code').isNull()).count()",
        f"print(f'Unmatched regional offices: {{unmatched}}')",
        f"",
        f"# Show sample with zonal codes",
        f"registry_df.select('Registration_ID', 'Regional_Office', 'Zonal_Area_Code', 'Zone_Description').show(10)",
        f"```",
        f"",
        f"**📖 Line-by-line explanation:**",
        f"- `broadcast(zonal_df)`: Tells Spark to send a complete copy of the small DataFrame to every ",
        f"  worker node. This avoids an expensive shuffle of the large registry DataFrame.",
        f"- `on='Regional_Office'`: The join key — rows are matched where the office names are equal.",
        f"- `how='left'`: A left join keeps all registry rows, even if no zonal match is found (the ",
        f"  zonal columns would be NULL for unmatched rows).",
        f"",
        f"**⚡ Performance insight:**",
        f"Without `broadcast()`, Spark would shuffle both DataFrames across the network — moving ~50,000 ",
        f"rows. With `broadcast()`, only the 20-row lookup table is copied. This is orders of magnitude ",
        f"faster and uses far less memory.",
        f"",
        f"**💡 Why this matters for DVLA:**",
        f"Every vehicle record now carries its 2026 Zonal Area Code, enabling decentralized reporting ",
        f"without needing to look up the mapping each time.",
    ]))
    cells.append(make_code_cell([
        f"# Step 7: Broadcast Join",
        f"# Type your code below",
        f"",
    ]))

    # =========================================================================
    # CELL 9: Step 8 — Prepare Payments & Flag Anomalies
    # =========================================================================
    cells.append(make_markdown_cell([
        f"## Step 8: Prepare Payment Data and Flag Revenue Anomalies",
        f"",
        f"**📋 What you will do:**",
        f"Clean the payment dataset and add a `Revenue_Flag` column that categorizes each transaction ",
        f"as CLEAN, ZERO_OR_NEGATIVE, or based on the payment amount.",
        f"",
        f"**🔧 Code to type:**",
        f"```python",
        f"# Add Revenue_Flag based on payment amount",
        f"payments_df = payments_df.withColumn(",
        f"    'Revenue_Flag',",
        f"    F.when(F.col('Amount_Paid_GHS') <= 0, 'ZERO_OR_NEGATIVE')",
        f"     .otherwise('CLEAN')",
        f")",
        f"",
        f"# Verify: count by revenue flag",
        f"payments_df.groupBy('Revenue_Flag').count().show()",
        f"```",
        f"",
        f"**📖 Line-by-line explanation:**",
        f"- `F.when(condition, value).otherwise(value)`: Creates a new column using conditional logic.",
        f"- Payments with amount ≤ 0 are flagged as `ZERO_OR_NEGATIVE`. All others are `CLEAN`.",
        f"- The `.groupBy().count()` verification shows how many transactions fall into each category.",
        f"",
        f"**💡 Why this matters for DVLA:**",
        f"This Revenue_Flag column becomes the basis for the 'Revenue Assurance & Leakage Map' in our ",
        f"dashboard. Deputy Director Albert can filter to see only flagged transactions for investigation.",
    ]))
    cells.append(make_code_cell([
        f"# Step 8: Prepare Payments and Flag Anomalies",
        f"# Type your code below",
        f"",
    ]))

    # =========================================================================
    # CELL 10: Step 9 — Window Function (Latest Payment)
    # =========================================================================
    cells.append(make_markdown_cell([
        f"## Step 9: Extract the Latest Payment Per Vehicle (Window Function)",
        f"",
        f"**📋 What you will do:**",
        f"Use a PySpark Window function to find the most recent payment transaction for each vehicle. ",
        f"This is essential for tracking active verification status.",
        f"",
        f"**🔧 Code to type:**",
        f"```python",
        f"# Define a window: partition by Registration_ID, order by timestamp descending",
        f"payment_window = Window.partitionBy('Registration_ID').orderBy(F.desc('Payment_Timestamp'))",
        f"",
        f"# Add a row number within each partition (1 = most recent)",
        f"payments_ranked = payments_df.withColumn(",
        f"    'row_num',",
        f"    F.row_number().over(payment_window)",
        f")",
        f"",
        f"# Keep only the latest payment per vehicle (row_num = 1)",
        f"latest_payments = payments_ranked.filter(F.col('row_num') == 1).drop('row_num')",
        f"",
        f"# Rename columns to indicate these are the 'latest' values",
        f"latest_payments = latest_payments \\",
        f"    .withColumnRenamed('Transaction_ID', 'Latest_Transaction_ID') \\",
        f"    .withColumnRenamed('Amount_Paid_GHS', 'Latest_Amount_Paid_GHS') \\",
        f"    .withColumnRenamed('Payment_Channel', 'Latest_Payment_Channel') \\",
        f"    .withColumnRenamed('Payment_Timestamp', 'Latest_Payment_Timestamp') \\",
        f"    .withColumnRenamed('Revenue_Flag', 'Revenue_Flag')",
        f"",
        f"print(f'Unique vehicles with payments: {{latest_payments.count():,}}')",
        f"latest_payments.show(5)",
        f"```",
        f"",
        f"**📖 Line-by-line explanation:**",
        f"- `Window.partitionBy('Registration_ID')`: Groups rows by vehicle. Each vehicle gets its own ",
        f"  'window' of payment records.",
        f"- `.orderBy(F.desc('Payment_Timestamp'))`: Within each window, sorts payments from newest to ",
        f"  oldest. The most recent payment gets position 1.",
        f"- `F.row_number().over(window)`: Assigns sequential integers (1, 2, 3...) within each window.",
        f"- `.filter(F.col('row_num') == 1)`: Keeps only the top row (most recent) per vehicle.",
        f"",
        f"**💡 Why this matters for DVLA:**",
        f"A vehicle may have multiple payment records (initial registration, annual renewals). We need ",
        f"the latest one to determine current compliance status. The window function does this ",
        f"efficiently without writing complex subqueries.",
    ]))
    cells.append(make_code_cell([
        f"# Step 9: Window Function — Latest Payment Per Vehicle",
        f"# Type your code below",
        f"",
    ]))

    # =========================================================================
    # CELL 11: Step 10 — Join Registry with Latest Payments
    # =========================================================================
    cells.append(make_markdown_cell([
        f"## Step 10: Join Registry with Latest Payments",
        f"",
        f"**📋 What you will do:**",
        f"Left join the cleaned vehicle registry with the latest payment records. Vehicles with no ",
        f"payment will be flagged as `NO_PAYMENT_RECORD`. Orphan payments (those with Registration_IDs ",
        f"not in the registry) will be flagged as `ORPHAN_PAYMENT`.",
        f"",
        f"**🔧 Code to type:**",
        f"```python",
        f"# Left join: keep all vehicles, attach their latest payment",
        f"final_df = registry_df.join(",
        f"    latest_payments,",
        f"    on='Registration_ID',",
        f"    how='left'",
        f")",
        f"",
        f"# Update Revenue_Flag for vehicles with no payment record",
        f"final_df = final_df.withColumn(",
        f"    'Revenue_Flag',",
        f"    F.when(F.col('Latest_Transaction_ID').isNull(), 'NO_PAYMENT_RECORD')",
        f"     .otherwise(F.col('Revenue_Flag'))",
        f")",
        f"",
        f"# Show the distribution of revenue flags",
        f"final_df.groupBy('Revenue_Flag').count().orderBy('count', ascending=False).show()",
        f"print(f'Final dataset rows: {{final_df.count():,}}')",
        f"```",
        f"",
        f"**📖 Line-by-line explanation:**",
        f"- `how='left'`: All registry vehicles are kept. If a vehicle has no matching payment, the ",
        f"  payment columns will be NULL.",
        f"- `F.when(F.col('Latest_Transaction_ID').isNull(), 'NO_PAYMENT_RECORD')`: Vehicles with no ",
        f"  payment get this flag. This could indicate a vehicle that was registered but never paid ",
        f"  fees — a compliance issue.",
        f"- `.otherwise(F.col('Revenue_Flag'))`: Preserves the existing flag (CLEAN or ZERO_OR_NEGATIVE) ",
        f"  for vehicles that do have a payment record.",
        f"",
        f"**💡 Why this matters for DVLA:**",
        f"The final Revenue_Flag provides a complete picture: CLEAN (legitimate), ZERO_OR_NEGATIVE ",
        f"(suspicious), NO_PAYMENT_RECORD (compliance gap). This directly feeds the Revenue Assurance ",
        f"dashboard view.",
    ]))
    cells.append(make_code_cell([
        f"# Step 10: Join Registry with Latest Payments",
        f"# Type your code below",
        f"",
    ]))

    # =========================================================================
    # CELL 12: Step 11 — Create Output Directory
    # =========================================================================
    cells.append(make_markdown_cell([
        f"## Step 11: Create Output Directory",
        f"",
        f"**📋 What you will do:**",
        f"Create the `./output/` directory within your workspace to store the cleaned data files.",
        f"",
        f"**🔧 Code to type:**",
        f"```python",
        f"# Create output directories",
        f"os.makedirs('./output/parquet', exist_ok=True)",
        f"print('✅ Output directory created: ./output/')",
        f"```",
        f"",
        f"**📖 Line-by-line explanation:**",
        f"- `os.makedirs(path, exist_ok=True)`: Creates the directory and all parent directories. ",
        f"  `exist_ok=True` prevents an error if the directory already exists.",
    ]))
    cells.append(make_code_cell([
        f"# Step 11: Create Output Directory",
        f"# Type your code below",
        f"",
    ]))

    # =========================================================================
    # CELL 13: Step 12 — Write Partitioned Parquet
    # =========================================================================
    cells.append(make_markdown_cell([
        f"## Step 12: Save as Partitioned Parquet Files",
        f"",
        f"**📋 What you will do:**",
        f"Save the cleaned dataset as partitioned Parquet files. Parquet is a columnar storage format ",
        f"optimized for analytical queries — it compresses data significantly and enables fast reads.",
        f"",
        f"**🔧 Code to type:**",
        f"```python",
        f"# Write partitioned Parquet files (organized by Zonal Area Code)",
        f"final_df.write \\",
        f"    .mode('overwrite') \\",
        f"    .partitionBy('Zonal_Area_Code') \\",
        f"    .parquet('./output/parquet/')",
        f"",
        f"print('✅ Parquet files saved to ./output/parquet/')",
        f"```",
        f"",
        f"**📖 Line-by-line explanation:**",
        f"- `.write`: Initiates a write operation on the DataFrame.",
        f"- `.mode('overwrite')`: Replaces any existing files in the output directory.",
        f"- `.partitionBy('Zonal_Area_Code')`: Creates subdirectories for each zone (e.g., ",
        f"  `Zonal_Area_Code=ACC-Z1/`, `Zonal_Area_Code=ASH-Z1/`). This enables partition pruning — ",
        f"  queries targeting a specific zone only read that folder.",
        f"- `.parquet(path)`: Writes in Apache Parquet format.",
        f"",
        f"**💡 Why this matters for DVLA:**",
        f"Parquet files are the standard format for big data pipelines. They are 5-10x smaller than ",
        f"CSV and can be read directly by Spark, Athena, BigQuery, and other analytics tools.",
    ]))
    cells.append(make_code_cell([
        f"# Step 12: Save as Partitioned Parquet",
        f"# Type your code below",
        f"",
    ]))

    # =========================================================================
    # CELL 14: Step 13 — Write Flat CSV for Power BI
    # =========================================================================
    cells.append(make_markdown_cell([
        f"## Step 13: Export Clean Data as a Flat CSV for Power BI",
        f"",
        f"**📋 What you will do:**",
        f"Convert the Spark DataFrame to a Pandas DataFrame and save it as a single flat CSV file. ",
        f"This is necessary because Spark's `.write.csv()` creates a directory with multiple part files, ",
        f"which Power BI cannot read directly.",
        f"",
        f"**🔧 Code to type:**",
        f"```python",
        f"# Convert Spark DataFrame to Pandas and save as a single CSV",
        f"# This consolidates all distributed data to a single node",
        f"final_pandas = final_df.toPandas()",
        f"final_pandas.to_csv('./output/powerbi_ready.csv', index=False, encoding='utf-8')",
        f"",
        f"print(f'✅ Saved {{len(final_pandas):,}} rows to ./output/powerbi_ready.csv')",
        f"print(f'Columns: {{list(final_pandas.columns)}}')",
        f"```",
        f"",
        f"**📖 Line-by-line explanation:**",
        f"- `.toPandas()`: Collects all data from the distributed Spark DataFrame to a single-node ",
        f"  Pandas DataFrame. **Warning**: This works here because our dataset is small (~50K rows). ",
        f"  For millions of rows, you would need a different approach.",
        f"- `.to_csv(path, index=False, encoding='utf-8')`: Saves as a standard CSV file. `index=False` ",
        f"  prevents Pandas from adding a row number column. `encoding='utf-8'` ensures Ghanaian names ",
        f"  with special characters are preserved correctly.",
        f"",
        f"**⚠️ Why not use Spark's .write.csv()?**",
        f"Spark's `.write.csv()` creates a directory containing multiple files like `part-00000.csv`, ",
        f"`part-00001.csv`, plus a `_SUCCESS` marker file. Power BI and Streamlit expect a single file ",
        f"at a known path — not a directory of parts.",
    ]))
    cells.append(make_code_cell([
        f"# Step 13: Export as Flat CSV",
        f"# Type your code below",
        f"",
    ]))

    # =========================================================================
    # CELL 15: Step 14 — Validation
    # =========================================================================
    cells.append(make_markdown_cell([
        f"## Step 14: Validate the Clean Output",
        f"",
        f"**📋 What you will do:**",
        f"Run validation checks to confirm the ETL pipeline produced correct results.",
        f"",
        f"**🔧 Code to type:**",
        f"```python",
        f"import pandas as pd",
        f"",
        f"# Reload the saved CSV and validate",
        f"validation_df = pd.read_csv('./output/powerbi_ready.csv', encoding='utf-8')",
        f"",
        f"print('=== VALIDATION REPORT ===')",
        f"print(f'Total rows:           {{len(validation_df):,}}')",
        f"print(f'Total columns:        {{len(validation_df.columns)}}')",
        f"print(f'Columns:              {{list(validation_df.columns)}}')",
        f"print()",
        f"",
        f"# Check for expected columns",
        f"expected_cols = ['Registration_ID', 'Chassis_Number', 'Owner_Name', 'National_ID_Number',",
        f"                 'Registration_Date', 'Vehicle_Make', 'Regional_Office',",
        f"                 'Zonal_Area_Code', 'Zone_Description', 'Identity_Status']",
        f"missing = [c for c in expected_cols if c not in validation_df.columns]",
        f"print(f'Missing expected columns: {{missing if missing else \"None ✅\"}}')",
        f"print()",
        f"",
        f"# Check data completeness",
        f"if 'Zonal_Area_Code' in validation_df.columns:",
        f"    null_zones = validation_df['Zonal_Area_Code'].isna().sum()",
        f"    print(f'Null Zonal_Area_Code: {{null_zones}} (should be 0)')",
        f"",
        f"if 'Identity_Status' in validation_df.columns:",
        f"    print(f'Identity breakdown:')",
        f"    print(validation_df['Identity_Status'].value_counts().to_string())",
        f"print()",
        f"",
        f"if 'Revenue_Flag' in validation_df.columns:",
        f"    print(f'Revenue flag breakdown:')",
        f"    print(validation_df['Revenue_Flag'].value_counts().to_string())",
        f"",
        f"print()",
        f"print('✅ Validation complete!')",
        f"```",
        f"",
        f"**📖 Explanation:**",
        f"This validation step confirms that:",
        f"- The output file exists and is readable",
        f"- All expected columns are present",
        f"- Zonal Area Codes were successfully assigned (no nulls)",
        f"- Identity and Revenue flags are populated",
    ]))
    cells.append(make_code_cell([
        f"# Step 14: Validate the Clean Output",
        f"# Type your code below",
        f"",
    ]))

    # =========================================================================
    # CELL 16: Step 15 — Stop Spark
    # =========================================================================
    cells.append(make_markdown_cell([
        f"## Step 15: Stop the SparkSession",
        f"",
        f"**📋 What you will do:**",
        f"Shut down the SparkSession to release JVM memory and resources.",
        f"",
        f"**🔧 Code to type:**",
        f"```python",
        f"# Stop the SparkSession to free memory",
        f"spark.stop()",
        f"print('✅ SparkSession stopped. JVM resources released.')",
        f"```",
        f"",
        f"**📖 Explanation:**",
        f"- `spark.stop()`: Shuts down the Spark driver process and frees the 2GB of JVM memory. ",
        f"  This is **critical** on a shared server — if you don't stop Spark, the memory remains ",
        f"  allocated and other students may not be able to start their sessions.",
        f"",
        f"> ⚠️ **Always run this cell when you finish Lab 2!**",
    ]))
    cells.append(make_code_cell([
        f"# Step 15: Stop the SparkSession",
        f"# Type your code below",
        f"",
    ]))

    # =========================================================================
    # CELL 17: Step 16 — Power BI Instructions
    # =========================================================================
    cells.append(make_markdown_cell([
        f"## 📊 Next Steps: Downloading Data & Building a Power BI Star Schema",
        f"",
        f"Congratulations, {student_name}! You have completed the ETL pipeline. Your clean data is now ",
        f"saved at `./output/powerbi_ready.csv`.",
        f"",
        f"### Step A: Download Your Clean CSV File",
        f"",
        f"1. In the **JupyterLab sidebar** (left panel), click the 📁 file browser icon.",
        f"2. Navigate to your workspace folder → `output/`.",
        f"3. Right-click on `powerbi_ready.csv`.",
        f"4. Select **\"Download\"** from the context menu.",
        f"5. The file will be saved to your **Windows 11 Downloads folder**.",
        f"",
        f"### Step B: Import into Power BI Desktop",
        f"",
        f"1. Open **Power BI Desktop** on your Windows 11 machine.",
        f"2. Click **Home → Get Data → Text/CSV**.",
        f"3. Browse to your Downloads folder and select `powerbi_ready.csv`.",
        f"4. In the preview dialog, verify the column types look correct, then click **Load**.",
        f"",
        f"### Step C: Build a Star Schema Data Model",
        f"",
        f"A **Star Schema** is a database design pattern optimized for analytical reporting. It consists of:",
        f"- **Fact Table**: The main data table containing measures (amounts, counts).",
        f"- **Dimension Tables**: Small lookup tables for filtering and grouping.",
        f"",
        f"**To create the Star Schema:**",
        f"",
        f"1. After importing `powerbi_ready.csv`, go to the **Model view** (left sidebar icon).",
        f"2. Your imported data becomes the **Fact Table** (`powerbi_ready`).",
        f"3. Create a **Zonal Lookup Dimension Table**:",
        f"   - Click **Home → Enter Data**.",
        f"   - Create a table named `Dim_Zonal_Lookup` with columns: `Zonal_Area_Code`, `Zone_Description`, `Region`.",
        f"   - Fill in the 10 unique zonal codes from the mapping (ACC-Z1, ACC-Z2, etc.).",
        f"4. **Create the Relationship**:",
        f"   - In the Model view, drag `Zonal_Area_Code` from the Fact Table to `Zonal_Area_Code` in `Dim_Zonal_Lookup`.",
        f"   - Set cardinality to **Many-to-One (N:1)** — many vehicles belong to one zone.",
        f"   - Set cross-filter direction to **Single**.",
        f"",
        f"### Star Schema Diagram",
        f"",
        f"```",
        f"                    ┌──────────────────────┐",
        f"                    │   Dim_Zonal_Lookup   │",
        f"                    │──────────────────────│",
        f"                    │ Zonal_Area_Code (PK) │",
        f"                    │ Zone_Description     │",
        f"                    │ Region               │",
        f"                    └─────────┬────────────┘",
        f"                              │  1:N",
        f"                    ┌─────────┴────────────┐",
        f"                    │   powerbi_ready      │",
        f"                    │   (Fact Table)        │",
        f"                    │──────────────────────│",
        f"                    │ Registration_ID      │",
        f"                    │ Zonal_Area_Code (FK) │",
        f"                    │ Latest_Amount_Paid   │",
        f"                    │ Revenue_Flag         │",
        f"                    │ Identity_Status      │",
        f"                    │ ...                  │",
        f"                    └──────────────────────┘",
        f"```",
        f"",
        f"---",
        f"*Lab 2 Complete — Well done, {student_name}! 🎉*",
        f"",
        f"*You can now view your results on the Streamlit dashboard or continue to build ",
        f"your Power BI report.*",
    ]))

    return nb


# =============================================================================
# MAIN EXECUTION
# =============================================================================

def main():
    """
    Main entry point. Creates workspace directories for all four profiles
    and generates all three lab notebooks in each.
    """
    print("=" * 70)
    print("  DVLA Ghana Big Data Lab -- Notebook Builder")
    print("  Generating Lab 0, Lab 1 & Lab 2 for all workspaces")
    print("=" * 70)

    for folder, name, role in WORKSPACES:
        workspace_dir = os.path.join(BASE_DIR, folder)
        os.makedirs(workspace_dir, exist_ok=True)
        print(f"\n[BUILD] Building notebooks for: {name} ({role}) -> ./{folder}/")

        # Build and save Lab 0
        lab0 = build_lab0(name, role, folder)
        lab0_path = os.path.join(workspace_dir, "Lab0_Big_Data_SQL_and_ETL_Basics.ipynb")
        save_notebook(lab0, lab0_path)

        # Build and save Lab 1
        lab1 = build_lab1(name, role, folder)
        lab1_path = os.path.join(workspace_dir, "Lab1_SQL_Profiling_and_Extraction.ipynb")
        save_notebook(lab1, lab1_path)

        # Build and save Lab 2
        lab2 = build_lab2(name, role)
        lab2_path = os.path.join(workspace_dir, "Lab2_PySpark_ETL_and_Transformation.ipynb")
        save_notebook(lab2, lab2_path)

    # --- Print summary ---
    print("\n" + "=" * 70)
    print("  NOTEBOOK GENERATION SUMMARY")
    print("=" * 70)
    for folder, name, role in WORKSPACES:
        lab0_exists = os.path.exists(os.path.join(BASE_DIR, folder, "Lab0_Big_Data_SQL_and_ETL_Basics.ipynb"))
        lab1_exists = os.path.exists(os.path.join(BASE_DIR, folder, "Lab1_SQL_Profiling_and_Extraction.ipynb"))
        lab2_exists = os.path.exists(os.path.join(BASE_DIR, folder, "Lab2_PySpark_ETL_and_Transformation.ipynb"))
        print(f"  {name:25s} Lab0: {'[OK]' if lab0_exists else '[FAIL]'}  Lab1: {'[OK]' if lab1_exists else '[FAIL]'}  Lab2: {'[OK]' if lab2_exists else '[FAIL]'}")

    # --- Validate JSON integrity ---
    print(f"\n  Validating notebook JSON integrity...")
    errors = 0
    for folder, name, role in WORKSPACES:
        for nb_name in ["Lab0_Big_Data_SQL_and_ETL_Basics.ipynb", "Lab1_SQL_Profiling_and_Extraction.ipynb", "Lab2_PySpark_ETL_and_Transformation.ipynb"]:
            nb_path = os.path.join(BASE_DIR, folder, nb_name)
            try:
                with open(nb_path, "r", encoding="utf-8") as f:
                    nb_data = json.load(f)
                assert nb_data.get("nbformat") == 4, "Wrong nbformat"
                assert "cells" in nb_data, "Missing cells"
                assert len(nb_data["cells"]) > 0, "No cells"
                assert "kernelspec" in nb_data.get("metadata", {}), "Missing kernelspec"
            except Exception as e:
                print(f"  [FAIL] {folder}/{nb_name}: {e}")
                errors += 1

    if errors == 0:
        print(f"  [OK] All 12 notebooks passed JSON integrity validation!")
    else:
        print(f"  [WARN] {errors} notebook(s) failed validation.")

    total_notebooks = len(WORKSPACES) * 3
    print(f"\n  Total notebooks generated: {total_notebooks}")
    print("=" * 70)


if __name__ == "__main__":
    main()
