# Implementation Plan: DVLA Ghana Big Data Practical Lab

This updated implementation plan outlines the deliverables for the 2-day practical big data training lab tailored for the Research, Business Development & Innovation (RBDI) department of the Driver and Vehicle Licensing Authority (DVLA) Ghana, under Director Abraham Zaato. The participants are:
- **Benjamin Y. Peh** (Manager, Intermediate, MIS)
- **Albert Wotorgbui** (Deputy Director, Intermediate)
- **Peter Djameshie** (Officer, Beginner)

The lab models an end-to-end local ETL data processing engine focused on legacy data cleanup, revenue protection, and 2026 Zonal Area Code harmonization.

## User Review Required

> [!IMPORTANT]
> **Environment Specifications & Resource Caps**:
> - The target deployment host is a headless Ubuntu 24 server running multi-tenant student environments.
> - **Spark Driver Memory Cap**: Capped strictly at **2GB** (`spark.driver.memory = "2g"`) to prevent OOM kernel panics when all three sessions run concurrently.
> - **Directory Structure**:
>   ├── `raw_data/`                          <-- Shared read-only source directory (e.g. `../raw_data/` relative to notebooks)
>   ├── `benjamin/`                          <-- Isolated workspace for Student 1
>   │   ├── `Lab1_SQL_Profiling_and_Extraction.ipynb`
>   │   ├── `Lab2_PySpark_ETL_and_Transformation.ipynb`
>   │   └── `output/powerbi_ready.csv`
>   ├── `albert/`                            <-- Isolated workspace for Student 2
>   └── `peter/`                             <-- Isolated workspace for Student 3
>
> **2026 Zonal Area Code dictionary mapping**:
> Regional branches mapped to new 2026 Zonal Area Codes:
> - **Accra (Greater Accra)**: ACC-Z1 (Central), ACC-Z2 (West), ACC-Z3 (East), ACC-Z4 (Tema)
>   - Accra, Weija, Tema, 37
> - **Kumasi (Ashanti)**: ASH-Z1 (Metro), ASH-Z2 (Outer)
>   - Kumasi, Obuasi, Mampong
> - **Tamale (Northern)**: NOR-Z1 (Northern)
>   - Tamale
> - **Takoradi (Western)**: WES-Z1 (Western)
>   - Takoradi, Tarkwa
> - **Cape Coast (Central)**: CEN-Z1 (Central)
>   - Cape Coast, Winneba
> - **Koforidua (Eastern)**: EAS-Z1 (Eastern)
>   - Koforidua, Nkawkaw
> - **Sunyani (Bono)**: BON-Z1 (Bono)
>   - Sunyani, Techiman
> - **Bolgatanga (Upper East)**: UPE-Z1 (Upper East)
>   - Bolgatanga
> - **Wa (Upper West)**: UPW-Z1 (Upper West)
>   - Wa
> - **Ho (Volta)**: VOL-Z1 (Volta)
>   - Ho, Aflao
>
> **Jupyter Notebook Pedagogical Design**:
> - **Guided Notebook Structure**: Instead of empty prompts, the notebooks will utilize a guided workflow.
> - **Comprehensive Markdown Cells**: For each step, the notebook will have a markdown cell displaying the exact Python/SQL code for the student to write, a line-by-line explanation of every parameter/function, and the technical logic/business case behind that step (e.g., why duplicates leak revenue, why broadcast joins save memory).
> - **Blank/Template Code Cells**: Immediately following each markdown guide, there will be a corresponding code cell where students type and execute the shown code.
>
> **Streamlit Dynamic Loading & Raw-vs-Clean Toggle**:
> - **Dynamic Updates**: Once a student completes `Lab2_PySpark_ETL_and_Transformation.ipynb` and writes their data to `./{student}/output/powerbi_ready.csv`, the Streamlit application immediately and automatically loads and updates that student's dashboard view. Friendly warnings will be displayed if a student's file does not exist yet.
> - **Raw vs. Clean Toggle**: The sidebar will feature a **"Data Source Selection"** toggle:
>   - **Raw Legacy Data**: Loads and processes the uncleaned files directly from `raw_data/` to show the pre-ETL dashboard state (e.g., duplicate entries, uncleaned date structures, missing IDs, active revenue leaks).
>   - **Clean Transformed Data**: Loads the selected student's `./{student}/output/powerbi_ready.csv` file, showing the post-ETL dashboard state. This allows a direct "before vs. after" quality comparison.

## Proposed Changes

### Central Data & Scripts

#### [NEW] [generate_dvla_data.py](file:///c:/Users/PRTG/Documents/AG/dvla_big_data_lab/generate_dvla_data.py)
A standalone Python script utilizing `pandas` to generate two large, realistic datasets (50,000+ rows each) inside the central `raw_data/` folder.
- **Dataset 1: `legacy_vehicle_registry.csv`**:
  - Columns: `Registration_ID`, `Chassis_Number`, `Owner_Name`, `National_ID_Number`, `Registration_Date`, `Vehicle_Make`, `Regional_Office`.
  - Anomalies: 5% duplicates, 10% null IDs, mixed date formats (`YYYY-MM-DD` and `DD/MM/YYYY`).
- **Dataset 2: `payment_transaction_log.csv`**:
  - Columns: `Transaction_ID`, `Registration_ID`, `Amount_Paid_GHS`, `Payment_Timestamp`, `Payment_Channel`.
  - Anomalies: Orphan payments, negative/zero amounts, duplicate transaction logs.

#### [NEW] [build_notebooks.py](file:///c:/Users/PRTG/Documents/AG/dvla_big_data_lab/build_notebooks.py)
A programmatic generator script that writes the `.ipynb` notebook JSON structure for each of the three students.
- **`Lab1_SQL_Profiling_and_Extraction.ipynb`**:
  - **DuckDB Connection Setup**: Initialize DuckDB, load CSVs, and inspect schemas.
  - **SQL Query Steps**: Formulate queries (`COUNT`, `GROUP BY`, `HAVING`) to isolate anomalies.
  - **Instruction Format**: Clear description of the syntax, detailing what DuckDB does under the hood, and prompting the student to execute the query.
- **`Lab2_PySpark_ETL_and_Transformation.ipynb`**:
  - **Spark Architecture & 2GB Limit**: Explains JVM/executor memory and configures driver baseline.
  - **PySpark ETL Steps**: Standardize columns, drop duplicates, replace null values with `'UNVERIFIED_HOLDER'`, parse date formats.
  - **Broadcast Join**: Join mapping table to 2026 Zonal Area Code dictionary.
  - **Window Function**: Get latest payment record.
  - **Power BI / Star Schema Instructions**: Step-by-step instructions for downloading output and modeling data.

#### [NEW] [dvla_dashboard.py](file:///c:/Users/PRTG/Documents/AG/dvla_big_data_lab/dvla_dashboard.py)
Streamlit application template configured as a multi-tenant hub. Allows picking a student workspace, toggling between **Raw Legacy Data** and **Clean Transformed Data** sources, and toggling between three views:
- **View 1**: Data Cleansing & Quality Audit.
- **View 2**: Revenue Assurance & Leakage Map.
- **View 3**: 2026 Zonal Registration Metrics.

---

## Verification Plan

### Automated Verification
1. **Execution Check on Generator**: Run `python generate_dvla_data.py`.
2. **Execution Check on Notebook Builder**: Run `python build_notebooks.py`.
3. **Notebook JSON Integrity**: Verify `.ipynb` files can be read by `json.loads`.

### Manual Verification
1. **Interactive Dashboard**: Run Streamlit locally (`streamlit run dvla_dashboard.py`).
