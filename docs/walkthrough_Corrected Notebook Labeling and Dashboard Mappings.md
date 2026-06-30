# Walkthrough: Corrected Notebook Labeling and Dashboard Mappings

This walkthrough documents the assessment, implementation, and verification of the notebook labeling issue and the Streamlit mapping for the DVLA Big Data Lab.

## Summary of Changes

### 1. Updated Notebook Builder Template
We modified [build_notebooks.py](file:///c:/Users/PRTG/Documents/AG/dvla_big_data_lab/build_notebooks.py) to dynamically reference the correct workspace folder of the occupant in Lab 1. 

- Previously, the template was hardcoded with `./benjamin/` as a static example:
  ```python
  f"  This works because your notebook is inside your personal workspace folder (e.g., `./benjamin/`)."
  ```
- We updated the `build_lab1` function to accept the `student_folder` parameter and dynamically populate it:
  ```python
  f"  This works because your notebook is inside your personal workspace folder (e.g., `./{student_folder}/`)."
  ```
- We updated the main generator loop to pass the current workspace folder name `folder` when invoking `build_lab1`:
  ```python
  lab1 = build_lab1(name, role, folder)
  ```

### 2. Regenerated All Workspace Notebooks
We ran the modified `build_notebooks.py` script to regenerate all 8 notebooks across the four directories (`kevin/`, `benjamin/`, `albert/`, `peter/`).

---

## Verification and Results

### Notebook Verification
We performed a grep search across all `.ipynb` files to verify that `benjamin` is no longer incorrectly referenced in the other participants' notebooks. 

The results show that each participant's notebook is now correctly labeled with their specific workspace folder:
* **Peter**: [peter/Lab1_SQL_Profiling_and_Extraction.ipynb](file:///c:/Users/PRTG/Documents/AG/dvla_big_data_lab/peter/Lab1_SQL_Profiling_and_Extraction.ipynb#L137)
  ```json
  "  This works because your notebook is inside your personal workspace folder (e.g., `./peter/`)."
  ```
* **Albert**: [albert/Lab1_SQL_Profiling_and_Extraction.ipynb](file:///c:/Users/PRTG/Documents/AG/dvla_big_data_lab/albert/Lab1_SQL_Profiling_and_Extraction.ipynb#L137)
  ```json
  "  This works because your notebook is inside your personal workspace folder (e.g., `./albert/`)."
  ```
* **Kevin**: [kevin/Lab1_SQL_Profiling_and_Extraction.ipynb](file:///c:/Users/PRTG/Documents/AG/dvla_big_data_lab/kevin/Lab1_SQL_Profiling_and_Extraction.ipynb#L137)
  ```json
  "  This works because your notebook is inside your personal workspace folder (e.g., `./kevin/`)."
  ```
* **Benjamin**: [benjamin/Lab1_SQL_Profiling_and_Extraction.ipynb](file:///c:/Users/PRTG/Documents/AG/dvla_big_data_lab/benjamin/Lab1_SQL_Profiling_and_Extraction.ipynb#L137)
  ```json
  "  This works because your notebook is inside your personal workspace folder (e.g., `./benjamin/`)."
  ```

---

### Streamlit Dashboard Mapping Verification
We assessed [dvla_dashboard.py](file:///c:/Users/PRTG/Documents/AG/dvla_big_data_lab/dvla_dashboard.py) to ensure that the clean datasets each participant will produce will map correctly to their respective dashboards.

1. **Workspace Options**: The application imports workspace options directly from the keys of the `WORKSPACES` dictionary:
   ```python
   WORKSPACES = {
       "kevin": "Kevin (Instructor)",
       "benjamin": "Benjamin Y. Peh",
       "albert": "Albert Wotorgbui",
       "peter": "Peter Djameshie",
   }
   ```
2. **Dynamic File Resolution**: When a user selects a workspace (e.g., `peter` for Peter Djameshie), the app resolves the clean file path dynamically in `load_clean_data(student_folder)` using the active `workspace_key`:
   ```python
   csv_path = os.path.join(BASE_DIR, student_folder, "output", "powerbi_ready.csv")
   ```
   This ensures that Peter's dashboard will load exactly `./peter/output/powerbi_ready.csv`, and other participants' dashboards are similarly mapped to their respective folders.
