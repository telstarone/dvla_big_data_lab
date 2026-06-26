# Walkthrough: DVLA Ghana Big Data Practical Lab

## Summary

Successfully generated the complete codebase for a 2-day practical big data training lab for the DVLA Ghana RBDI department. The lab infrastructure consists of 4 workspace profiles, 2 raw datasets, 8 guided Jupyter Notebooks, and 1 multi-tenant Streamlit dashboard.

## Files Created

### Root Scripts

| File | Size | Purpose |
|---|---|---|
| [requirements.txt](file:///c:/Users/PRTG/Documents/AG/dvla_big_data_lab/requirements.txt) | 985 B | Python dependency manifest (pandas, duckdb, pyspark, streamlit, pyarrow) |
| [generate_dvla_data.py](file:///c:/Users/PRTG/Documents/AG/dvla_big_data_lab/generate_dvla_data.py) | 21 KB | Data generation engine with deterministic seeding and anomaly injection |
| [build_notebooks.py](file:///c:/Users/PRTG/Documents/AG/dvla_big_data_lab/build_notebooks.py) | 78 KB | Programmatic Jupyter Notebook builder for 4 workspaces |
| [dvla_dashboard.py](file:///c:/Users/PRTG/Documents/AG/dvla_big_data_lab/dvla_dashboard.py) | 23 KB | Multi-tenant Streamlit dashboard with 3 analytical views |

### Generated Datasets

| File | Rows | Size |
|---|---|---|
| [legacy_vehicle_registry.csv](file:///c:/Users/PRTG/Documents/AG/dvla_big_data_lab/raw_data/legacy_vehicle_registry.csv) | 52,500 | 4.4 MB |
| [payment_transaction_log.csv](file:///c:/Users/PRTG/Documents/AG/dvla_big_data_lab/raw_data/payment_transaction_log.csv) | 52,500 | 3.3 MB |

### Generated Notebooks (8 total)

| Workspace | Lab 1 (DuckDB SQL) | Lab 2 (PySpark ETL) |
|---|---|---|
| [kevin/](file:///c:/Users/PRTG/Documents/AG/dvla_big_data_lab/kevin) | [Lab1](file:///c:/Users/PRTG/Documents/AG/dvla_big_data_lab/kevin/Lab1_SQL_Profiling_and_Extraction.ipynb) (25 KB) | [Lab2](file:///c:/Users/PRTG/Documents/AG/dvla_big_data_lab/kevin/Lab2_PySpark_ETL_and_Transformation.ipynb) (39 KB) |
| [benjamin/](file:///c:/Users/PRTG/Documents/AG/dvla_big_data_lab/benjamin) | [Lab1](file:///c:/Users/PRTG/Documents/AG/dvla_big_data_lab/benjamin/Lab1_SQL_Profiling_and_Extraction.ipynb) (25 KB) | [Lab2](file:///c:/Users/PRTG/Documents/AG/dvla_big_data_lab/benjamin/Lab2_PySpark_ETL_and_Transformation.ipynb) (39 KB) |
| [albert/](file:///c:/Users/PRTG/Documents/AG/dvla_big_data_lab/albert) | [Lab1](file:///c:/Users/PRTG/Documents/AG/dvla_big_data_lab/albert/Lab1_SQL_Profiling_and_Extraction.ipynb) (25 KB) | [Lab2](file:///c:/Users/PRTG/Documents/AG/dvla_big_data_lab/albert/Lab2_PySpark_ETL_and_Transformation.ipynb) (39 KB) |
| [peter/](file:///c:/Users/PRTG/Documents/AG/dvla_big_data_lab/peter) | [Lab1](file:///c:/Users/PRTG/Documents/AG/dvla_big_data_lab/peter/Lab1_SQL_Profiling_and_Extraction.ipynb) (25 KB) | [Lab2](file:///c:/Users/PRTG/Documents/AG/dvla_big_data_lab/peter/Lab2_PySpark_ETL_and_Transformation.ipynb) (39 KB) |

## Data Generation Verification

The data generator confirmed correct anomaly injection rates:

| Metric | Target | Actual |
|---|---|---|
| Registry duplicate rows | ~5% | 4.8% (2,500 rows) |
| Null National_ID_Number | ~10% | 9.9% (5,221 entries) |
| Mixed date formats | ~30% | 30.0% (15,766 entries) |
| Payment duplicate rows | ~5% | 4.8% (2,500 rows) |
| Orphan payments | ~10% | 10.0% (5,252 rows) |
| Zero/negative amounts | ~5% | 5.0% (2,628 rows) |

## Notebook Validation

All 8 notebooks passed JSON integrity validation:
- nbformat: v4 confirmed
- kernelspec: Python 3 present
- Cell structure: markdown + code cell pairs for each guided step

## Technical Decisions

1. **Windows cp1252 encoding**: Print statements use ASCII-safe markers (`[OK]`, `[BUILD]`) instead of Unicode emoji to avoid `UnicodeEncodeError` on Windows consoles. The notebook markdown cells retain full Unicode/emoji since Jupyter renders them in a web browser (UTF-8).

2. **Deterministic seeding**: `random.seed(2026)` and `np.random.seed(2026)` ensure identical datasets on every run.

3. **Spark driver memory**: Capped at 2GB per the implementation plan to prevent OOM when 4 sessions run concurrently.

4. **Single-file CSV export**: Lab2 uses `.toPandas().to_csv()` instead of Spark's `.write.csv()` to produce a single flat file compatible with Power BI and Streamlit.

5. **Safe date parsing**: Dashboard uses `pd.to_datetime(errors='coerce')` with `format='mixed'` and `dayfirst=True` to safely handle the intentionally mixed date formats in raw data.

6. **Altair row limits**: Dashboard pre-aggregates data via `groupby()` before passing to Altair charts, avoiding the 5,000-row default limit.

## How to Use

```bash
# 1. Install dependencies (on Ubuntu server)
pip install -r requirements.txt

# 2. Generate raw datasets (run once)
python generate_dvla_data.py

# 3. Generate student notebooks (run once)
python build_notebooks.py

# 4. Launch dashboard
streamlit run dvla_dashboard.py

# 5. Students open JupyterLab and work through:
#    - Lab1_SQL_Profiling_and_Extraction.ipynb
#    - Lab2_PySpark_ETL_and_Transformation.ipynb
```
