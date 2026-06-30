# Implementation Plan: Lab 0 (Intro to Big Data, SQL, and ETL Basics)

This plan outlines the creation and integration of a new beginner-friendly **Lab 0** notebook across all four user workspaces (`kevin`, `benjamin`, `albert`, `peter`). 

Lab 0 will introduce participants to foundational concepts (Big Data, SQL, and ETL) using DuckDB and standard Python/pandas, establishing a smooth learning curve before they progress to DuckDB SQL profiling (Lab 1) and PySpark ETL pipelines (Lab 2).

---

## Notebook Curriculum Design

Lab 0 will be broken down into structured, beginner-friendly steps with detailed explanations, visual aids (markdown diagrams/tables), step-by-step instructions, and hands-on exercises:

1. **Introduction to Big Data & Databases**:
   - High-level overview: OLTP (transactions) vs. OLAP (analytics).
   - What are databases, tables, rows, columns, and schemas?
   - Formats: CSV vs. JSON.
2. **Step 1: Setting up the environment**:
   - Installing/importing DuckDB and pandas.
   - Creating in-memory data tables for practice.
3. **Step 2: Basic SQL Queries**:
   - Selecting all columns (`SELECT *`).
   - Selecting specific columns.
   - Sorting rows (`ORDER BY`).
   - Restricting results (`LIMIT`).
4. **Step 3: Filtering Data (`WHERE` clause)**:
   - Filtering on exact text, numeric thresholds, and multiple conditions (`AND`, `OR`).
5. **Step 4: SQL Aggregations & Grouping**:
   - Summarizing data: `COUNT`, `SUM`, `AVG`.
   - Aggregating by category: `GROUP BY` and `HAVING`.
6. **Step 5: Joining Tables (`JOIN` clause)**:
   - Visualizing how separate tables relate (primary keys vs. foreign keys).
   - Performing an `INNER JOIN` between `vehicles` and `owners`.
7. **Step 6: Introduction to ETL (Extract, Transform, Load)**:
   - Concept breakdown: Extract (read), Transform (clean/calculate), Load (write).
   - Hands-on Python exercise using `pandas`:
     - **Extract**: Load raw mock data.
     - **Transform**: Clean null fields, format text, calculate values.
     - **Load**: Write out a clean CSV dataset.

---

## Proposed Changes

### Notebook Generation Script

#### [MODIFY] [build_notebooks.py](file:///c:/Users/PRTG/Documents/AG/dvla_big_data_lab/build_notebooks.py)
We will:
- Implement a new helper function `build_lab0(student_name: str, role: str, student_folder: str) -> dict` that programmatically builds the Lab 0 notebook using cells containing Markdown explanations and placeholder code blocks.
- Update `main()` to generate and save `Lab0_Big_Data_SQL_and_ETL_Basics.ipynb` for each workspace:
  ```python
  lab0 = build_lab0(name, role, folder)
  lab0_path = os.path.join(workspace_dir, "Lab0_Big_Data_SQL_and_ETL_Basics.ipynb")
  save_notebook(lab0, lab0_path)
  ```
- Update the generation summary prints and JSON validation logic to support the new notebook.

---

### Workspace Notebooks

#### [NEW] [Lab0_Big_Data_SQL_and_ETL_Basics.ipynb](file:///c:/Users/PRTG/Documents/AG/dvla_big_data_lab/peter/Lab0_Big_Data_SQL_and_ETL_Basics.ipynb) (and respective paths for `kevin/`, `benjamin/`, `albert/`)
The script will write a new notebook file in each directory.

---

### Project Documentation & Scripts

#### [MODIFY] [README.md](file:///c:/Users/PRTG/Documents/AG/dvla_big_data_lab/README.md)
Update the curriculum description and the workspace files table to include the new Lab 0 notebook.

#### [MODIFY] [deploy_setup.sh](file:///c:/Users/PRTG/Documents/AG/dvla_big_data_lab/deploy_setup.sh)
Update log messages to reflect that 12 notebooks (3 per workspace across 4 workspaces) are generated instead of 8.

---

## Verification Plan

### Automated Verification
- Run `python build_notebooks.py` locally.
- Confirm all 12 notebooks are generated successfully (`[OK]` status printed for all).
- Confirm JSON validation passes for all generated notebooks.

### Manual Verification
- Review the generated Lab 0 notebook JSON structure to confirm that personalization features (e.g. `student_name`, `role`, and `student_folder`) are correctly substituted.
