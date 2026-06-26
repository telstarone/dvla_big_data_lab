# Implementation Plan: DVLA Ghana Big Data Practical Lab (Hardened)

This implementation plan outlines the deliverables for the 2-day practical big data training lab tailored for the Research, Business Development & Innovation (RBDI) department of the Driver and Vehicle Licensing Authority (DVLA) Ghana, under Director Abraham Zaato. The participants are:
- **Kevin** (Lab Instructor — pre-flight validation workspace)
- **Benjamin Y. Peh** (Manager, Intermediate, MIS)
- **Albert Wotorgbui** (Deputy Director, Intermediate)
- **Peter Djameshie** (Officer, Beginner)

The lab models an end-to-end local ETL data processing engine focused on legacy data cleanup, revenue protection, and 2026 Zonal Area Code harmonization.

---

## User Review Required

> [!IMPORTANT]
> **Environment Specifications & Resource Caps**:
> - Target deployment host: **headless Ubuntu 24** server.
> - Development machine: **Windows 11** (scripts must use cross-platform `os.path.join()` / `pathlib.Path`).
> - **Spark Driver Memory**: Strictly **2GB** (`spark.driver.memory = "2g"`) to prevent OOM kernel panics when all 4 sessions (1 instructor + 3 students) run concurrently.
> - **Python packages required on Ubuntu server**: `pandas`, `duckdb`, `pyspark`, `streamlit`, `altair` (bundled with streamlit), `pyarrow`.

> [!WARNING]
> **Altair Row Limit**: Altair's default max rows is 5,000. With 50,000+ row datasets, all chart rendering must either aggregate data before passing to Altair, or use `alt.data_transformers.disable_max_rows()`. The plan uses pre-aggregation (safer, faster).

### Directory Structure (Multi-Tenant)
```
dvla_big_data_lab/
├── raw_data/                              <-- Shared read-only source (generated once)
│   ├── legacy_vehicle_registry.csv
│   └── payment_transaction_log.csv
├── kevin/                                 <-- Lab Instructor (pre-flight validation)
│   ├── Lab1_SQL_Profiling_and_Extraction.ipynb
│   ├── Lab2_PySpark_ETL_and_Transformation.ipynb
│   └── output/
│       ├── parquet/                        <-- Partitioned Parquet (written by Spark)
│       └── powerbi_ready.csv              <-- Single flat file (written by .toPandas())
├── benjamin/                              <-- Student 1 workspace (identical structure)
├── albert/                                <-- Student 2 workspace (identical structure)
├── peter/                                 <-- Student 3 workspace (identical structure)
├── generate_dvla_data.py                  <-- Task 1: Data generator
├── build_notebooks.py                     <-- Task 2: Notebook builder
├── dvla_dashboard.py                      <-- Task 3: Streamlit dashboard
└── requirements.txt                       <-- Dependency manifest
```

### 2026 Zonal Area Code Dictionary
Regional branches mapped to new 2026 Zonal Area Codes (used in broadcast join):

| Regional_Office | Zonal_Area_Code | Zone_Description |
|---|---|---|
| Accra Metro | ACC-Z1 | Central Accra |
| Weija | ACC-Z2 | West Accra |
| Madina | ACC-Z3 | East Accra |
| Tema | ACC-Z4 | Tema Industrial |
| Kumasi | ASH-Z1 | Kumasi Metro |
| Obuasi | ASH-Z2 | Ashanti South |
| Mampong | ASH-Z2 | Ashanti North |
| Tamale | NOR-Z1 | Northern Metro |
| Takoradi | WES-Z1 | Sekondi-Takoradi |
| Tarkwa | WES-Z1 | Western Mining Belt |
| Cape Coast | CEN-Z1 | Central Metro |
| Winneba | CEN-Z1 | Central Coast |
| Koforidua | EAS-Z1 | Eastern Metro |
| Nkawkaw | EAS-Z1 | Eastern Highlands |
| Sunyani | BON-Z1 | Bono Metro |
| Techiman | BON-Z1 | Bono East |
| Bolgatanga | UPE-Z1 | Upper East Metro |
| Wa | UPW-Z1 | Upper West Metro |
| Ho | VOL-Z1 | Volta Metro |
| Aflao | VOL-Z1 | Volta Border |

### Output Schema for `powerbi_ready.csv`
The final clean CSV written by Lab2 must contain these exact columns (this is the contract between the notebook and the dashboard):

| Column | Type | Description |
|---|---|---|
| `Registration_ID` | string | Deduplicated vehicle registration identifier |
| `Chassis_Number` | string | 17-character VIN |
| `Owner_Name` | string | Registered owner |
| `National_ID_Number` | string | Ghana Card number or `UNVERIFIED_HOLDER` |
| `Registration_Date` | string (YYYY-MM-DD) | Standardized date |
| `Vehicle_Make` | string | Manufacturer |
| `Regional_Office` | string | Original branch |
| `Zonal_Area_Code` | string | 2026 zone code from broadcast join |
| `Zone_Description` | string | Human-readable zone name |
| `Latest_Transaction_ID` | string | Most recent payment ID (from window function) |
| `Latest_Amount_Paid_GHS` | float | Most recent payment amount |
| `Latest_Payment_Channel` | string | Channel of most recent payment |
| `Latest_Payment_Timestamp` | string | Timestamp of most recent payment |
| `Identity_Status` | string | `VERIFIED` or `UNVERIFIED_HOLDER` |
| `Revenue_Flag` | string | `CLEAN`, `ZERO_OR_NEGATIVE`, `ORPHAN_PAYMENT`, or `NO_PAYMENT_RECORD` |

### Technical Corrections Incorporated
1. **PySpark Single-File Output**: Use `.toPandas().to_csv("./output/powerbi_ready.csv", index=False)` instead of `.write.csv()` which creates multi-part directories. Partitioned Parquet is still written via Spark's native `.write.parquet()` (directory output is the expected Parquet format).
2. **Safe Date Parsing**: Dashboard uses `pd.to_datetime(col, format='mixed', dayfirst=True, errors='coerce')` for raw data — mixed date formats safely coerced to `NaT`.
3. **Spark Session Cleanup**: Each Lab2 notebook ends with `spark.stop()` to release JVM resources for other students.
4. **Deterministic Seeding**: `generate_dvla_data.py` uses `random.seed(2026)` and `np.random.seed(2026)` for reproducible datasets across all runs.
5. **Output Directory Auto-Creation**: Notebooks include `os.makedirs("./output", exist_ok=True)` before writing.
6. **Altair Aggregation**: Dashboard pre-aggregates data with `groupby()` before charting to stay within Altair's row limits.

---

## Proposed Changes

### [NEW] [requirements.txt](file:///c:/Users/PRTG/Documents/AG/dvla_big_data_lab/requirements.txt)
Dependency manifest for the Ubuntu 24 server:
```
pandas>=2.0
duckdb>=0.9
pyspark>=3.5
streamlit>=1.30
pyarrow>=14.0
```

---

### [NEW] [generate_dvla_data.py](file:///c:/Users/PRTG/Documents/AG/dvla_big_data_lab/generate_dvla_data.py)
Standalone Python script using `pandas` to generate two realistic datasets (50,000+ clean rows each, plus injected anomalies) inside `raw_data/`.

**Dataset 1 — `legacy_vehicle_registry.csv`** (~52,500 rows after anomaly injection):
- **50,000 base rows** generated with:
  - `Registration_ID`: Ghanaian plate format `GR-NNNN-YY`, `GW-NNNN-YY`, `GN-NNNN-YY` etc.
  - `Chassis_Number`: Realistic 17-character alphanumeric VIN strings.
  - `Owner_Name`: Pool of ~200 realistic Ghanaian names (Akan, Ewe, Ga, Dagbani surnames).
  - `National_ID_Number`: Ghana Card format `GHA-NNNNNNNNN-N`.
  - `Registration_Date`: Random dates 2015–2025.
  - `Vehicle_Make`: Weighted random from `[Toyota, Hyundai, Nissan, Honda, Kia, Mercedes-Benz, Ford, Volkswagen, Suzuki, Mitsubishi]`.
  - `Regional_Office`: Weighted random from the 20 branches in the Zonal dictionary.
- **Anomaly injections**:
  - **5% exact duplicate rows** (~2,500 rows randomly sampled and appended).
  - **10% null `National_ID_Number`** (~5,000 entries set to `NaN`).
  - **30% mixed date format** (~15,000 entries reformatted from `YYYY-MM-DD` to `DD/MM/YYYY`).
- **Encoding**: UTF-8 explicit.
- **Deterministic**: `random.seed(2026)`.

**Dataset 2 — `payment_transaction_log.csv`** (~55,000 rows after anomaly injection):
- **50,000 base rows** generated with:
  - `Transaction_ID`: Format `TXN-NNNNNNNN`.
  - `Registration_ID`: 90% drawn from registry IDs (valid linkage), 10% orphaned (non-existent IDs).
  - `Amount_Paid_GHS`: Normal distribution centered around GHS 350 (range ~50–5000), representing vehicle registration/renewal fees.
  - `Payment_Timestamp`: Random datetimes 2020–2025 in ISO 8601 format.
  - `Payment_Channel`: Weighted random from `[MTN MoMo, Telecel Cash, AT Money, e-Levy Portal, Bank Branch]`.
- **Anomaly injections**:
  - **~5,000 orphan payments** (10%): `Registration_ID` values not present in the vehicle registry.
  - **~2,500 zero/negative amounts** (5%): `Amount_Paid_GHS` set to `0` or random negative values.
  - **~2,500 duplicate transactions** (5%): Exact duplicate rows appended.

---

### [NEW] [build_notebooks.py](file:///c:/Users/PRTG/Documents/AG/dvla_big_data_lab/build_notebooks.py)
Programmatic generator that creates **4 workspace directories** (`./kevin/`, `./benjamin/`, `./albert/`, `./peter/`) and writes two `.ipynb` files per workspace. Kevin's notebooks are identical in content and serve as the instructor's pre-flight validation environment — used to execute the full lab pipeline and verify all outputs before students begin. Each notebook uses `nbformat` v4.5 JSON structure with correct `kernelspec` metadata for Python 3.

**Pedagogical Design Pattern** (applied to every step in both notebooks):
```
┌─────────────────────────────────────────────────────┐
│  MARKDOWN CELL: Step N — [Title]                    │
│  ─────────────────────────────────────────────────  │
│  📋 What you will do:                               │
│     [Plain English description of the step]         │
│                                                     │
│  🔧 Code to type:                                   │
│     ```python                                       │
│     [Exact code block for student to type]          │
│     ```                                             │
│                                                     │
│  📖 Line-by-line explanation:                       │
│     - `line 1`: [what it does and why]              │
│     - `line 2`: [what it does and why]              │
│                                                     │
│  💡 Why this matters for DVLA:                      │
│     [Business context / data engineering rationale] │
├─────────────────────────────────────────────────────┤
│  CODE CELL: (empty — student types here)            │
│     # Step N: [Title]                               │
│     # Type your code below                          │
└─────────────────────────────────────────────────────┘
```

**Notebook 1 — `Lab1_SQL_Profiling_and_Extraction.ipynb`** (~12 cell pairs):
1. Welcome & Context markdown (personalized with student name).
2. Install/import DuckDB.
3. Create in-memory connection and load both CSVs from `../raw_data/`.
4. `DESCRIBE` / `PRAGMA table_info` — inspect schemas.
5. Basic profiling: `COUNT(*)`, `COUNT(DISTINCT ...)`, `MIN/MAX` dates.
6. Duplicate detection: `GROUP BY ALL HAVING COUNT(*) > 1`.
7. Null ID profiling: `COUNT(*) WHERE National_ID_Number IS NULL`.
8. Payment anomaly: `WHERE Amount_Paid_GHS <= 0`.
9. Orphan detection: `LEFT JOIN ... WHERE registry.Registration_ID IS NULL`.
10. Summary statistics: aggregate anomaly counts per `Regional_Office`.
11. Discussion markdown: what these findings mean for DVLA's data cleanup initiative.

**Notebook 2 — `Lab2_PySpark_ETL_and_Transformation.ipynb`** (~18 cell pairs):
1. Welcome & Spark architecture explainer (lazy evaluation, DAG, driver vs. executors).
2. Import libraries and create `SparkSession` with `spark.driver.memory = "2g"`.
3. Load both CSVs with `spark.read.csv(..., header=True, inferSchema=True)`.
4. Inspect schemas: `printSchema()`, `count()`.
5. Deduplication: `dropDuplicates()` — explain shuffle cost.
6. Null handling: `fillna({'National_ID_Number': 'UNVERIFIED_HOLDER'})`, add `Identity_Status` column.
7. Date standardization: PySpark `coalesce(to_date(col, 'yyyy-MM-dd'), to_date(col, 'dd/MM/yyyy'))`.
8. Define the 2026 Zonal Area Code dictionary as a Python list of dicts → Spark DataFrame.
9. `broadcast()` join: explain why broadcast is optimal for small lookup tables.
10. Load payments, deduplicate, flag zero/negative amounts.
11. Window function: `row_number().over(Window.partitionBy("Registration_ID").orderBy(desc("Payment_Timestamp")))` — extract latest payment per vehicle.
12. Left join registry with latest payments, tag `Revenue_Flag` for anomalies.
13. `os.makedirs("./output", exist_ok=True)`.
14. Write partitioned Parquet: `df.write.mode("overwrite").partitionBy("Zonal_Area_Code").parquet("./output/parquet/")`.
15. Write single flat CSV: `df.toPandas().to_csv("./output/powerbi_ready.csv", index=False)`.
16. Validation queries: count rows, verify no nulls in key columns, confirm zonal codes populated.
17. `spark.stop()` — release JVM resources.
18. **Closing markdown**: Step-by-step instructions for downloading `powerbi_ready.csv` via JupyterLab sidebar, importing into Power BI Desktop, and building a **Star Schema** (fact table `powerbi_ready` linked to dimension table `Zonal_Lookup` via `Zonal_Area_Code` in a 1:N relationship).

---

### [NEW] [dvla_dashboard.py](file:///c:/Users/PRTG/Documents/AG/dvla_big_data_lab/dvla_dashboard.py)
Multi-tenant Streamlit dashboard hub with robust error handling, `@st.cache_data` caching, and pre-aggregated charting.

**Sidebar Controls**:
- **Dropdown A — Workspace**: `kevin (Instructor)`, `benjamin`, `albert`, `peter`.
- **Data Source Toggle**: Radio button switching between `📊 Raw Legacy Data` and `✅ Clean Transformed Data`.
- **Dropdown B — Dashboard View**: Three views selectable.

**Raw Data Loading Logic** (when "Raw Legacy Data" selected):
- Reads both CSVs from `raw_data/` and performs an in-memory `pd.merge()` left join on `Registration_ID`.
- Applies `pd.to_datetime(col, format='mixed', dayfirst=True, errors='coerce')` for safe date parsing.
- Computes anomaly flags inline (duplicates, nulls, orphans, zero amounts) as temporary columns.
- **View 3 unavailable in raw mode** (no `Zonal_Area_Code` exists yet) — shows an informational banner explaining the column is created during Lab2.

**Clean Data Loading Logic** (when "Clean Transformed Data" selected):
- Reads `./{student}/output/powerbi_ready.csv`.
- If file doesn't exist: displays a friendly `st.warning()` banner with instructions to complete Lab2 first. Does not crash.

**View 1 — Data Cleansing & Quality Audit**:
- KPI row: Total rows, data completeness % (non-null National_ID), duplicates eliminated count (raw count minus clean count).
- Bar chart: anomaly distribution by `Regional_Office` (pre-aggregated via `groupby`).

**View 2 — Revenue Assurance & Leakage Map**:
- KPI row: Total valid revenue (sum of `Amount_Paid_GHS > 0`), total flagged transactions, protected revenue %.
- Donut/pie chart: payment channel distribution.
- Alert table: `st.dataframe()` listing all rows where `Revenue_Flag != 'CLEAN'` with sortable columns.

**View 3 — 2026 Zonal Registration Metrics** (clean data only):
- Interactive bar chart: vehicle count per `Zonal_Area_Code`, colored by zone, sorted descending.
- Summary table: zone-level statistics (vehicle count, avg payment, % verified identities).

---

## Edge Cases & Robustness Measures

| # | Edge Case | Mitigation |
|---|---|---|
| 1 | Student hasn't run Lab2 yet — `powerbi_ready.csv` missing | Dashboard shows `st.warning()` with instructions, does not crash |
| 2 | `raw_data/` not generated yet | Dashboard shows `st.error()` prompting admin to run `generate_dvla_data.py` |
| 3 | Mixed date formats crash charting | `pd.to_datetime(errors='coerce')` converts unparseable to `NaT` |
| 4 | Altair >5000 row limit | All charts use pre-aggregated DataFrames (never raw 50k+ rows) |
| 5 | Spark `.write.csv()` creates directory not file | Lab2 uses `.toPandas().to_csv()` for flat file output |
| 6 | 4 concurrent Spark sessions OOM the server | Driver memory capped at 2GB; `spark.stop()` at end of Lab2 |
| 7 | Notebook paths break across OS | `os.path.join()` used everywhere; raw data referenced as `../raw_data/` |
| 8 | Non-deterministic data across runs | Fixed seed `random.seed(2026)` ensures identical datasets |
| 9 | DuckDB can't infer mixed-format dates | Lab1 treats `Registration_Date` as VARCHAR for profiling, not DATE |
| 10 | Orphan payments have no registry match | Left join in Lab2 tags these with `Revenue_Flag = 'ORPHAN_PAYMENT'` |
| 11 | `output/` directory doesn't exist | Notebooks include `os.makedirs("./output", exist_ok=True)` before write |
| 12 | View 3 selected with raw data (no zonal codes) | Dashboard disables View 3 in raw mode with explanatory banner |
| 13 | Empty DataFrames after aggressive filtering | All chart/table renders wrapped in `if len(df) > 0:` guards |
| 14 | CSV encoding issues with Ghanaian names | All reads/writes explicitly use `encoding='utf-8'` |

---

## Verification Plan

### Automated Verification
1. **Generator execution**: `python generate_dvla_data.py` — verify exit code 0.
2. **Row count check**: Verify `legacy_vehicle_registry.csv` has ≥52,000 rows and `payment_transaction_log.csv` has ≥52,000 rows.
3. **Anomaly percentage spot-check**: Script prints summary stats confirming ~5% duplicates, ~10% null IDs, ~5% orphan payments, ~5% zero/negative amounts.
4. **Notebook builder execution**: `python build_notebooks.py` — verify exit code 0.
5. **Notebook JSON integrity**: Load each `.ipynb` with `json.loads()` — verify `nbformat` v4, `kernelspec` present, cell types valid.
6. **Notebook cell count**: Verify Lab1 has ~24 cells (12 markdown + 12 code) and Lab2 has ~36 cells (18 markdown + 18 code).
7. **Directory structure**: Verify `kevin/`, `benjamin/`, `albert/`, `peter/` directories created with both notebooks in each.
8. **Instructor pre-flight**: Execute Kevin's Lab1 and Lab2 notebooks end-to-end in JupyterLab to confirm the full pipeline produces valid `kevin/output/powerbi_ready.csv`.
9. **Dashboard smoke test**: `streamlit run dvla_dashboard.py` — verify it starts without errors, Kevin's workspace shows clean data, and the raw data toggle works.

### Manual Verification
1. **Power BI flow**: Download `powerbi_ready.csv` and verify it imports cleanly into Power BI Desktop.
2. **Star Schema**: Confirm the Zonal lookup dimension can be split out and linked via 1:N relationship.
