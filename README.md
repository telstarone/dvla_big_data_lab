# DVLA Ghana: Big Data & Analytics Practical Lab
> **2-Day Hands-on Training Workshop | Research, Business Development & Innovation (RBDI) Department**

![DVLA Lab Banner](https://img.shields.io/badge/DVLA-Ghana_RBDI_Lab-blue.svg?style=for-the-badge&logo=apache-spark&logoColor=orange)
![Python](https://img.shields.io/badge/Python-3.12-3776AB.svg?style=for-the-badge&logo=python&logoColor=white)
![Spark](https://img.shields.io/badge/Apache_Spark-3.5-E25A2B.svg?style=for-the-badge&logo=apachespark&logoColor=white)
![DuckDB](https://img.shields.io/badge/DuckDB-0.9+-FFF000.svg?style=for-the-badge&logo=data:image/svg+xml;base64,...)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-FF4B4B.svg?style=for-the-badge&logo=streamlit&logoColor=white)

---

## 📋 Course & Workshop Overview

This repository houses the complete programmatic codebase for a **2-Day Practical Big Data Training Lab** custom-tailored for the **Driver and Vehicle Licensing Authority (DVLA) Ghana** under the leadership of **Director Abraham Zaato**.

The workshop is structured around an end-to-end local ETL processing engine modeled on actual business scenarios: **legacy registry data cleanup, revenue protection/leakage detection, and the 2026 Zonal Area Code harmonization initiative**.

### Participants & Target Personas

The lab is designed to accommodate three specific learning profiles within the RBDI department:
1. **Albert Wotorgbui (Deputy Director, Strategic/Intermediate)**: Focused on strategic revenue analysis, data governance, and high-level dashboard metrics.
2. **Benjamin Y. Peh (Manager, Intermediate/MIS)**: Focused on query optimizations, profiling legacy databases, and database consolidation.
3. **Peter Djameshie (Officer, Beginner)**: Structured walk-throughs introducing programmatic data transformations and scripting.
4. **Kevin (Instructor, Master)**: A dedicated folder pre-configured with solved notebooks to verify pipeline mechanics and validate dashboard integrations before launch.

---

## 🛠️ Repository Architecture

The project is structured into modular workspaces for each student, centralizing raw data generation and automated templates build:

```text
dvla_big_data_lab/
├── docs/
│   └── deployment_guide.md       # Step-by-step Apache/Ubuntu server deployment guide
├── raw_data/                     # Directory for generated relational mock datasets
│   ├── legacy_vehicle_registry.csv
│   └── payment_transaction_log.csv
├── kevin/                        # Instructor Workspace (Solved Labs validation)
│   ├── Lab0_Big_Data_SQL_and_ETL_Basics.ipynb
│   ├── Lab1_SQL_Profiling_and_Extraction.ipynb
│   └── Lab2_PySpark_ETL_and_Transformation.ipynb
├── benjamin/                     # Benjamin's Workspace (Manager, MIS)
├── albert/                       # Albert's Workspace (Deputy Director)
├── peter/                        # Peter's Workspace (Officer, Beginner)
├── build_notebooks.py            # Programmatic notebook compiler
├── generate_dvla_data.py         # Relational database mock data generation engine
├── dvla_dashboard.py             # Multi-tenant Streamlit monitoring dashboard
├── requirements.txt              # Unified Python dependency manifest
└── deploy_setup.sh               # Automated Ubuntu 24.04 server provisioning script
```

---

## 🔬 Lab Curriculum & Objectives

### Lab 0: Big Data, SQL & ETL Basics (Introductory Level)
* **Goal**: Teach absolute beginners the concepts of relational databases, basic SQL queries, and local ETL processes.
* **Core Tools**: `DuckDB` (in-process SQL engine) and `Pandas` (Python data manipulation).
* **Skills Covered**: SQL query structures (`SELECT`, `WHERE`, `ORDER BY`, `LIMIT`), aggregates & groupings (`COUNT`, `GROUP BY`), relational `JOIN` operations, and a mini Python/pandas ETL pipeline to clean and save a CSV.

### Day 1: SQL Profiling & Legacy Data Extraction (DuckDB)
* **Goal**: Analyze the anomalies, duplicates, missing values, and mixed format dates inside the raw database.
* **Core Tool**: `DuckDB` (in-process SQL OLAP engine).
* **Skills Covered**: Standard SQL queries, aggregate operations, regex parsing for National ID verification, and identifying missing transaction linkages (orphan payments).

### Day 2: Scalable ETL & Transformation (PySpark)
* **Goal**: Build a data cleanup and harmonization pipeline using Spark DataFrames.
* **Core Tool**: `PySpark` (Apache Spark Python API).
* **Skills Covered**: Data deduplication, schema enforcement, date standardization, window functions for latest payment extraction, and broadcast-joining regional offices to the new 2026 Zonal Area Codes.
* **Output**: A Power BI / Streamlit-compatible flattened CSV (`powerbi_ready.csv`) containing zero anomalies.

---

## 🚀 Local Quickstart Guide

To run the workshop codebase locally on a development machine (Windows, macOS, or Linux):

### 1. Prerequisites
Ensure you have **Python 3.10+** and a **Java Runtime Environment (JRE/JDK 8 or 17)** installed on your machine (Java is required for Spark).

### 2. Installation
Clone the repository and install the Python dependencies:
```bash
# Clone the repository
git clone https://github.com/telstarone/dvla_big_data_lab.git
cd dvla_big_data_lab

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate

# Install requirements
pip install -r requirements.txt
pip install jupyterlab
```

### 3. Generate Raw Data
Run the relational database mock engine to populate the `raw_data/` folder with 50,000+ records containing custom data anomalies (duplicates, null fields, date mismatches):
```bash
python generate_dvla_data.py
```

### 4. Build Workspace Notebooks
Run the notebook compiler to generate the Jupyter Notebook files custom-tailored for each student's profile:
```bash
python build_notebooks.py
```

### 5. Launch Services
Run JupyterLab to start working on the labs, and run Streamlit to launch the comparative analytics dashboard:
```bash
# Terminal A: Start JupyterLab
jupyter lab

# Terminal B: Start Streamlit Dashboard
streamlit run dvla_dashboard.py
```

---

## 🖥️ Streamlit Monitoring Dashboard

The Streamlit dashboard (`dvla_dashboard.py`) acts as a real-time validation screen for the training exercise. It allows students to toggle between:
1. **Raw Legacy Data**: Visually illustrates the anomalies, unverified national identities, and lost revenue leaks across offices.
2. **Clean Transformed Data**: Connects directly to the student's output file (`powerbi_ready.csv`) once they compile their PySpark ETL notebook. Toggling this view reveals the visual impact of their code (zero duplicates, 100% ID completeness, recovered revenue assurance mapping, and 2026 Zonal distribution charts).

---

## 🌐 Server Deployment Overview

For headless deployment on **Ubuntu 24.04 LTS** server running behind **Apache**:
1. Configure `dvla.hcs.co.ke` DNS records.
2. Clone the repository securely via SSH Keys or Personal Access Token (PAT).
3. Run the automated bash installer:
   ```bash
   sudo bash deploy_setup.sh
   ```
4. Secure the site using Let's Encrypt:
   ```bash
   sudo certbot --apache -d dvla.hcs.co.ke
   ```

Refer to the comprehensive [docs/deployment_guide.md](file:///c:/Users/PRTG/Documents/AG/dvla_big_data_lab/docs/deployment_guide.md) for full server configuration, systemd services management, and Apache reverse-proxy rules.
