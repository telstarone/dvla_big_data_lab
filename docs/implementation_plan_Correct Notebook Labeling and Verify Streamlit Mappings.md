# Correct Notebook Labeling and Verify Streamlit Mappings

The goal of this task is to:
1. Fix the Jupyter Notebook templates generated for each workspace so they correctly reference the occupant's specific workspace directory rather than defaulting/hardcoding `benjamin`.
2. Regenerate all 8 notebooks (Lab 1 & Lab 2) for the four workspaces (`kevin`, `benjamin`, `albert`, `peter`).
3. Thoroughly check all notebooks to ensure labeling is correct.
4. Verify that the Streamlit dashboard maps each participant's clean output to their dashboard view.

## Proposed Changes

### Notebook Generation Script

We will modify [build_notebooks.py](file:///c:/Users/PRTG/Documents/AG/dvla_big_data_lab/build_notebooks.py) to pass the workspace folder name into `build_lab1` and use it dynamically in the description cell that refers to the personal workspace folder.

---

### Notebooks Regeneration

We will run [build_notebooks.py](file:///c:/Users/PRTG/Documents/AG/dvla_big_data_lab/build_notebooks.py) to update all 8 notebooks across the four folders:
- [kevin/Lab1_SQL_Profiling_and_Extraction.ipynb](file:///c:/Users/PRTG/Documents/AG/dvla_big_data_lab/kevin/Lab1_SQL_Profiling_and_Extraction.ipynb)
- [kevin/Lab2_PySpark_ETL_and_Transformation.ipynb](file:///c:/Users/PRTG/Documents/AG/dvla_big_data_lab/kevin/Lab2_PySpark_ETL_and_Transformation.ipynb)
- [benjamin/Lab1_SQL_Profiling_and_Extraction.ipynb](file:///c:/Users/PRTG/Documents/AG/dvla_big_data_lab/benjamin/Lab1_SQL_Profiling_and_Extraction.ipynb)
- [benjamin/Lab2_PySpark_ETL_and_Transformation.ipynb](file:///c:/Users/PRTG/Documents/AG/dvla_big_data_lab/benjamin/Lab2_PySpark_ETL_and_Transformation.ipynb)
- [albert/Lab1_SQL_Profiling_and_Extraction.ipynb](file:///c:/Users/PRTG/Documents/AG/dvla_big_data_lab/albert/Lab1_SQL_Profiling_and_Extraction.ipynb)
- [albert/Lab2_PySpark_ETL_and_Transformation.ipynb](file:///c:/Users/PRTG/Documents/AG/dvla_big_data_lab/albert/Lab2_PySpark_ETL_and_Transformation.ipynb)
- [peter/Lab1_SQL_Profiling_and_Extraction.ipynb](file:///c:/Users/PRTG/Documents/AG/dvla_big_data_lab/peter/Lab1_SQL_Profiling_and_Extraction.ipynb)
- [peter/Lab2_PySpark_ETL_and_Transformation.ipynb](file:///c:/Users/PRTG/Documents/AG/dvla_big_data_lab/peter/Lab2_PySpark_ETL_and_Transformation.ipynb)

---

### Streamlit App Verification

We will verify that [dvla_dashboard.py](file:///c:/Users/PRTG/Documents/AG/dvla_big_data_lab/dvla_dashboard.py) loads clean data from the correct subdirectories for each user. Currently, `load_clean_data(workspace_key)` is defined as:
```python
csv_path = os.path.join(BASE_DIR, student_folder, "output", "powerbi_ready.csv")
```
This correctly resolves to:
- `./kevin/output/powerbi_ready.csv` for Kevin
- `./benjamin/output/powerbi_ready.csv` for Benjamin
- `./albert/output/powerbi_ready.csv` for Albert
- `./peter/output/powerbi_ready.csv` for Peter

We will inspect and make sure that no other parts of `dvla_dashboard.py` hardcode mappings or mix up directories.

## Verification Plan

### Automated/Execution Verification
- Run `python build_notebooks.py` to regenerate the notebooks.
- Check that the builder runs successfully without JSON syntax issues.
- Verify contents of [peter/Lab1_SQL_Profiling_and_Extraction.ipynb](file:///c:/Users/PRTG/Documents/AG/dvla_big_data_lab/peter/Lab1_SQL_Profiling_and_Extraction.ipynb) using `grep_search` to verify it refers to `./peter/` instead of `./benjamin/`.

### Manual/Visual Verification
- Run `streamlit run dvla_dashboard.py` (or verify its structure) to ensure page navigation is correct and all workspace selectors map properly to the respective folder's output files.
