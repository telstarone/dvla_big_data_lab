# Walkthrough: Lab 0 (Intro to Big Data, SQL & ETL) Implementation

This walkthrough details the addition and validation of the new **Lab 0** introductory workshop module.

## Changes Made

### 1. Updated the Notebook Generator Script
We added the [build_lab0](file:///c:/Users/PRTG/Documents/AG/dvla_big_data_lab/build_notebooks.py#L137-L380) function in `build_notebooks.py` to programmatically build the introductory notebook `Lab0_Big_Data_SQL_and_ETL_Basics.ipynb` with detailed explanations and exercises covering:
* **Big Data Basics**: Definitions, OLTP vs OLAP databases.
* **Environment Setup**: Pip installs and imports for DuckDB and Pandas.
* **Database Creation**: Creating temporary tables and inserting practice records.
* **SQL Querying**: Writing basic `SELECT`, `WHERE`, `ORDER BY`, `LIMIT` statements, aggregate operations (`COUNT`, `GROUP BY`), and relational table `JOIN` queries.
* **Python ETL**: Constructing a local end-to-end Python/pandas ETL pipeline to extract data, capitalize titles, handle missing/invalid numeric metrics, calculate zonal area codes, and save to a CSV (`./output/lab0_clean.csv`).

We also updated `main()` in [build_notebooks.py](file:///c:/Users/PRTG/Documents/AG/dvla_big_data_lab/build_notebooks.py#L1976-L2039) to generate, summarize, and validate the new notebook alongside Labs 1 and 2.

### 2. Updated Project Documentation
* **Curriculum Overview**: Updated [README.md](file:///c:/Users/PRTG/Documents/AG/dvla_big_data_lab/README.md#L52-L60) to describe the curriculum and learning outcomes of the introductory Lab 0 module.
* **Directory Structure Map**: Updated the repository directory tree diagram in [README.md](file:///c:/Users/PRTG/Documents/AG/dvla_big_data_lab/README.md#L37-L44) to include the new Lab 0 notebook within the workspace structure.

---

## Validation & Verification

### Automated Execution
We executed `python build_notebooks.py` to generate the workspace files. The command completed successfully with output validating the JSON integrity of all 12 notebooks:
```text
======================================================================
  NOTEBOOK GENERATION SUMMARY
======================================================================
  Kevin                     Lab0: [OK]  Lab1: [OK]  Lab2: [OK]
  Benjamin Y. Peh           Lab0: [OK]  Lab1: [OK]  Lab2: [OK]
  Albert Wotorgbui          Lab0: [OK]  Lab1: [OK]  Lab2: [OK]
  Peter Djameshie           Lab0: [OK]  Lab1: [OK]  Lab2: [OK]

  Validating notebook JSON integrity...
  [OK] All 12 notebooks passed JSON integrity validation!

  Total notebooks generated: 12
======================================================================
```

### Notebook Inspection
We inspected the generated notebook files to verify they correctly substitute student attributes:
* **Peter**: [peter/Lab0_Big_Data_SQL_and_ETL_Basics.ipynb](file:///c:/Users/PRTG/Documents/AG/dvla_big_data_lab/peter/Lab0_Big_Data_SQL_and_ETL_Basics.ipynb) is personalized with:
  - `"Welcome, Peter Djameshie! (Officer)"`
  - Workspace folder example path `(e.g., ./peter/)`
* **Albert**: [albert/Lab0_Big_Data_SQL_and_ETL_Basics.ipynb](file:///c:/Users/PRTG/Documents/AG/dvla_big_data_lab/albert/Lab0_Big_Data_SQL_and_ETL_Basics.ipynb) is personalized with:
  - `"Welcome, Albert Wotorgbui! (Deputy Director)"`
  - Workspace folder example path `(e.g., ./albert/)`
* **Benjamin**: [benjamin/Lab0_Big_Data_SQL_and_ETL_Basics.ipynb](file:///c:/Users/PRTG/Documents/AG/dvla_big_data_lab/benjamin/Lab0_Big_Data_SQL_and_ETL_Basics.ipynb) is personalized with:
  - `"Welcome, Benjamin Y. Peh! (Manager, MIS)"`
  - Workspace folder example path `(e.g., ./benjamin/)`
* **Kevin**: [kevin/Lab0_Big_Data_SQL_and_ETL_Basics.ipynb](file:///c:/Users/PRTG/Documents/AG/dvla_big_data_lab/kevin/Lab0_Big_Data_SQL_and_ETL_Basics.ipynb) is personalized with:
  - `"Welcome, Kevin! (Lab Instructor)"`
  - Workspace folder example path `(e.g., ./kevin/)`
