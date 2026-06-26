# Implementation Plan: DVLA Ghana Big Data Practical Lab

This implementation plan details the generation of a 2-day training lab codebase for the DVLA Ghana RBDI (Revenue Mobilization & Business Development Integration) department officials: Benjamin (Intermediate, MIS), Albert (Strategic/Deputy Director), and Peter (Beginner). The lab models a localized ETL data engine focusing on data cleanup, revenue protection, and 2026 Zonal Area Code harmonization.

## User Review Required

> [!IMPORTANT]
> The environment requires Python libraries: `pandas`, `duckdb`, `pyspark` (with Py4J/Java 8 or 11 installed locally for local SparkSession), and `streamlit`. 
> 
> - **Spark Driver Memory**: Capped at 4GB as requested (`spark.driver.memory` = `4g`).
> - **2026 Zonal Area Code Dictionary**: To perform high-performance broadcast joins, we define a mapping from regional offices to new 2026 Zonal Area Codes:
>   - **Accra (Greater Accra)**: ACC-Z1 (Central Accra), ACC-Z2 (Weija/West Accra), ACC-Z3 (37/East Accra), ACC-Z4 (Tema/East)
>   - **Kumasi (Ashanti)**: ASH-Z1 (Kumasi Metro), ASH-Z2 (Obuasi/Mampong)
>   - **Tamale (Northern)**: NOR-Z1 (Tamale Metro)
>   - **Takoradi (Western)**: WES-Z1 (Sekondi-Takoradi)
>   - **Cape Coast (Central)**: CEN-Z1 (Cape Coast Metro)
>   - **Koforidua (Eastern)**: EAS-Z1 (Koforidua Metro)
>   - **Sunyani (Bono)**: BON-Z1 (Sunyani Metro)
>   - **Bolgatanga (Upper East)**: UPE-Z1 (Bolgatanga Metro)
>   - **Wa (Upper West)**: UPW-Z1 (Wa Metro)
>   - **Ho (Volta)**: VOL-Z1 (Ho Metro)

## Proposed Changes

### Central Data & Scripts

#### [NEW] [generate_dvla_data.py](file:///c:/Users/PRTG/Documents/AG/dvla_big_data_lab/generate_dvla_data.py)
A standalone Python script utilizing `pandas` to generate two large, realistic datasets (50,000+ rows each) inside the central `raw_data/` folder.
- **Dataset 1: `legacy_vehicle_registry.csv`**:
  - Columns: `Registration_ID`, `Chassis_Number`, `Owner_Name`, `National_ID_Number`, `Registration_Date`, `Vehicle_Make`, `Regional_Office`.
  - Anomalies injected:
    - 5% duplicate records (identical rows).
    - 10% missing identification entries (null/blank `National_ID_Number`).
    - Mixed date formats: `YYYY-MM-DD` and `DD/MM/YYYY` (e.g. `2024-05-12` vs `12/05/2024`).
  - Realistic Ghanaian data: Regional offices matching major DVLA Ghana branches, vehicle makes common in Ghana (Toyota, Hyundai, Nissan, Honda, Kia, Mercedes-Benz).
- **Dataset 2: `payment_transaction_log.csv`**:
  - Columns: `Transaction_ID`, `Registration_ID`, `Amount_Paid_GHS`, `Payment_Timestamp`, `Payment_Channel`.
  - Anomalies injected (revenue leakage):
    - Orphan registration records (payment transactions referencing a `Registration_ID` not present in the vehicle registry).
    - Zero or negative amount values (`Amount_Paid_GHS` <= 0).
    - Duplicate transaction logs (same transaction IDs with varying details or exact duplicates).
  - Ghanaian payment channels: `MTN Mobile Money`, `Telecel Cash`, `AT Money`, `e-Levy Portal`, `Partner Bank Branch`, `POS Terminal`.

#### [NEW] [build_notebooks.py](file:///c:/Users/PRTG/Documents/AG/dvla_big_data_lab/build_notebooks.py)
A programmatic generator script that creates directories for the three students (`./benjamin/`, `./albert/`, `./peter/`) and writes two distinct Jupyter Notebooks in each.
- **`Lab1_SQL_Profiling_and_Extraction.ipynb`**:
  - **Context**: Focuses on profiling historical DVLA data using DuckDB in-memory tables.
  - **Tasks**:
    - Initialize an inline DuckDB connection (`import duckdb`).
    - Load `legacy_vehicle_registry.csv` and `payment_transaction_log.csv` into tables.
    - Write SQL queries (using `COUNT(*)`, `GROUP BY`, and `HAVING`) to find duplicates, count missing National ID numbers, find orphan payments, and isolate transactions where amount <= 0.
- **`Lab2_PySpark_ETL_and_Transformation.ipynb`**:
  - **Context**: Walking students through lazy evaluation, Spark architecture, and high-performance transformations.
  - **Tasks**:
    - Initialize `SparkSession` with `.config("spark.driver.memory", "4g")`.
    - Load CSV files.
    - Deduplicate datasets (`dropDuplicates()`).
    - Handle missing `National_ID_Number` by replacing with placeholder or flagging as unverified.
    - Standardize date formats using PySpark expressions.
    - Perform high-performance `broadcast()` join of the cleaned registry against the 2026 Zonal Area Code dictionary.
    - Use Window functions (`partitionBy("Registration_ID").orderBy(col("Payment_Timestamp").desc())`) to extract the latest active payment transaction per vehicle.
    - Write output as partitioned Parquet files (`output/parquet/`) and a flat CSV file (`output/powerbi_ready.csv`) for dashboard loading.

#### [NEW] [dvla_dashboard.py](file:///c:/Users/PRTG/Documents/AG/dvla_big_data_lab/dvla_dashboard.py)
A self-contained Streamlit dashboard application template designed to:
- Dynamically detect and allow the user to select which student's output (`./output/powerbi_ready.csv`) to visualize (e.g., Benjamin, Albert, or Peter).
- Display high-level metrics: total clean vehicle count, data completeness percentage, and total protected revenue flags (unresolved anomalies).
- Provide sidebar filters for Regional Office and 2026 Zonal Area Codes.
- Render interactive charts:
  - Bar chart showing vehicle allocations across the 2026 Zonal Area Codes.
  - Alert table showing details of unresolved transactional anomalies (e.g. payments <= 0, duplicates, orphans) for strategic review by Albert.

---

## Verification Plan

### Automated Verification
1. **Python Syntax and Style Checks**: Run code formatting and syntax checks.
2. **Execution Check on Generator**: Run `python generate_dvla_data.py` to ensure it successfully generates 50,000+ rows with target anomalies and outputs them to `raw_data/`.
3. **Execution Check on Notebook Builder**: Run `python build_notebooks.py` to verify the JSON ipynb outputs are syntax-valid and placed correctly.
4. **Notebook JSON Integrity**: Programmatically verify that the output `.ipynb` files can be read by `json.loads` and match Jupyter Notebook format specifications.

### Manual Verification
1. **Interactive Dashboard**: Run Streamlit locally (`streamlit run dvla_dashboard.py`) and check if the dashboard renders metrics, filters, and charts correctly.
