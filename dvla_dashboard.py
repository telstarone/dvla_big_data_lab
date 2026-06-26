#!/usr/bin/env python3
# =============================================================================
# dvla_dashboard.py
# =============================================================================
# DVLA Ghana Big Data Practical Lab -- Multi-Tenant Streamlit Dashboard
#
# Purpose:
#   Interactive web dashboard that visualizes DVLA vehicle registration and
#   payment data across multiple student workspaces. Supports toggling between
#   raw (pre-ETL) and clean (post-ETL) data views to demonstrate the impact
#   of the data cleanup pipeline.
#
# Features:
#   - Multi-tenant workspace selector (kevin, benjamin, albert, peter)
#   - Raw vs. Clean data source toggle
#   - View 1: Data Cleansing & Quality Audit
#   - View 2: Revenue Assurance & Leakage Map
#   - View 3: 2026 Zonal Registration Metrics
#
# Usage:
#   streamlit run dvla_dashboard.py
#
# Author:  Lab Infrastructure (auto-generated)
# Date:    June 2026
# =============================================================================

import os
import streamlit as st
import pandas as pd
import altair as alt

# =============================================================================
# PAGE CONFIGURATION
# =============================================================================
st.set_page_config(
    page_title="DVLA Ghana - Big Data Lab Dashboard",
    page_icon=":oncoming_automobile:",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =============================================================================
# CONSTANTS
# =============================================================================

# Base directory (where this script lives)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Workspace definitions: (folder_name, display_label)
WORKSPACES = {
    "kevin": "Kevin (Instructor)",
    "benjamin": "Benjamin Y. Peh",
    "albert": "Albert Wotorgbui",
    "peter": "Peter Djameshie",
}

# Raw data paths (relative to BASE_DIR)
RAW_REGISTRY_PATH = os.path.join(BASE_DIR, "raw_data", "legacy_vehicle_registry.csv")
RAW_PAYMENTS_PATH = os.path.join(BASE_DIR, "raw_data", "payment_transaction_log.csv")

# 2026 Zonal Area Code mapping (for raw data mode — applied inline)
ZONAL_MAPPING = {
    "Accra Metro": ("ACC-Z1", "Central Accra"),
    "Weija": ("ACC-Z2", "West Accra"),
    "Madina": ("ACC-Z3", "East Accra"),
    "Tema": ("ACC-Z4", "Tema Industrial"),
    "Kumasi": ("ASH-Z1", "Kumasi Metro"),
    "Obuasi": ("ASH-Z2", "Ashanti South"),
    "Mampong": ("ASH-Z2", "Ashanti North"),
    "Tamale": ("NOR-Z1", "Northern Metro"),
    "Takoradi": ("WES-Z1", "Sekondi-Takoradi"),
    "Tarkwa": ("WES-Z1", "Western Mining Belt"),
    "Cape Coast": ("CEN-Z1", "Central Metro"),
    "Winneba": ("CEN-Z1", "Central Coast"),
    "Koforidua": ("EAS-Z1", "Eastern Metro"),
    "Nkawkaw": ("EAS-Z1", "Eastern Highlands"),
    "Sunyani": ("BON-Z1", "Bono Metro"),
    "Techiman": ("BON-Z1", "Bono East"),
    "Bolgatanga": ("UPE-Z1", "Upper East Metro"),
    "Wa": ("UPW-Z1", "Upper West Metro"),
    "Ho": ("VOL-Z1", "Volta Metro"),
    "Aflao": ("VOL-Z1", "Volta Border"),
}


# =============================================================================
# DATA LOADING FUNCTIONS
# =============================================================================

@st.cache_data(ttl=30)
def load_raw_data():
    """
    Load and merge the raw (pre-ETL) legacy datasets.

    Reads both CSVs from raw_data/, merges them on Registration_ID,
    applies safe date parsing, and computes inline anomaly flags.

    The @st.cache_data decorator caches the result for 30 seconds to avoid
    re-reading the files on every interaction. TTL is short so students
    can re-generate data and see updates quickly.

    Returns:
        Tuple of (merged_df, registry_df, payments_df) or (None, None, None) on error.
    """
    try:
        # Read CSVs with explicit UTF-8 encoding
        registry = pd.read_csv(RAW_REGISTRY_PATH, encoding="utf-8")
        payments = pd.read_csv(RAW_PAYMENTS_PATH, encoding="utf-8")

        # Safe date parsing: coerce unparseable mixed-format dates to NaT
        # instead of crashing the dashboard charts
        registry["Registration_Date"] = pd.to_datetime(
            registry["Registration_Date"], format="mixed", dayfirst=True, errors="coerce"
        )
        payments["Payment_Timestamp"] = pd.to_datetime(
            payments["Payment_Timestamp"], errors="coerce"
        )

        # Merge on Registration_ID (left join from registry perspective)
        merged = registry.merge(payments, on="Registration_ID", how="left")

        # Compute inline anomaly flags for raw data
        merged["Identity_Status"] = merged["National_ID_Number"].apply(
            lambda x: "UNVERIFIED_HOLDER" if pd.isna(x) or str(x).strip() == "" else "VERIFIED"
        )
        merged["Revenue_Flag"] = "CLEAN"
        merged.loc[merged["Amount_Paid_GHS"].isna(), "Revenue_Flag"] = "NO_PAYMENT_RECORD"
        merged.loc[merged["Amount_Paid_GHS"] <= 0, "Revenue_Flag"] = "ZERO_OR_NEGATIVE"
        # Mark orphan payments (Registration_IDs starting with ORPHAN-)
        if "Registration_ID" in payments.columns:
            orphan_ids = set(payments[payments["Registration_ID"].str.startswith("ORPHAN-", na=False)]["Registration_ID"])
            merged.loc[merged["Registration_ID"].isin(orphan_ids), "Revenue_Flag"] = "ORPHAN_PAYMENT"

        return merged, registry, payments
    except FileNotFoundError:
        return None, None, None
    except Exception as e:
        st.error(f"Error loading raw data: {e}")
        return None, None, None


@st.cache_data(ttl=30)
def load_clean_data(student_folder):
    """
    Load a student's clean (post-ETL) dataset.

    Reads the powerbi_ready.csv file from the student's output directory.

    Parameters:
        student_folder: Name of the student workspace folder.

    Returns:
        A pandas DataFrame or None if the file doesn't exist.
    """
    csv_path = os.path.join(BASE_DIR, student_folder, "output", "powerbi_ready.csv")
    try:
        df = pd.read_csv(csv_path, encoding="utf-8")
        # Safe date parsing
        if "Registration_Date" in df.columns:
            df["Registration_Date"] = pd.to_datetime(
                df["Registration_Date"], format="mixed", dayfirst=True, errors="coerce"
            )
        if "Latest_Payment_Timestamp" in df.columns:
            df["Latest_Payment_Timestamp"] = pd.to_datetime(
                df["Latest_Payment_Timestamp"], errors="coerce"
            )
        return df
    except FileNotFoundError:
        return None
    except Exception as e:
        st.error(f"Error loading clean data for {student_folder}: {e}")
        return None


# =============================================================================
# DASHBOARD VIEWS
# =============================================================================

def render_view1_quality_audit(df, data_source, raw_registry=None):
    """
    View 1: Data Cleansing & Quality Audit

    Displays high-level KPI cards for data quality metrics and a bar chart
    showing anomaly distribution by regional branch.

    Parameters:
        df:            The active DataFrame (raw merged or clean).
        data_source:   'raw' or 'clean' (affects metric calculations).
        raw_registry:  The raw registry DataFrame (for calculating dedup counts in clean mode).
    """
    st.header("View 1: Data Cleansing & Quality Audit")
    st.markdown("---")

    # --- KPI Metrics ---
    total_rows = len(df)

    # Data completeness: percentage of records with a verified National ID
    if "Identity_Status" in df.columns:
        verified = (df["Identity_Status"] == "VERIFIED").sum()
        completeness_pct = (verified / total_rows * 100) if total_rows > 0 else 0
    elif "National_ID_Number" in df.columns:
        non_null = df["National_ID_Number"].notna().sum()
        completeness_pct = (non_null / total_rows * 100) if total_rows > 0 else 0
    else:
        completeness_pct = 0

    # Duplicates eliminated (only meaningful in clean mode with raw comparison)
    if data_source == "clean" and raw_registry is not None:
        dups_eliminated = len(raw_registry) - total_rows
    else:
        # In raw mode, count actual duplicates
        if total_rows > 0:
            unique_rows = df.drop_duplicates().shape[0]
            dups_eliminated = total_rows - unique_rows
        else:
            dups_eliminated = 0

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(
            label="Total Records",
            value=f"{total_rows:,}",
            delta=f"-{dups_eliminated:,} duplicates" if data_source == "clean" else None,
        )
    with col2:
        st.metric(
            label="Data Completeness (National ID)",
            value=f"{completeness_pct:.1f}%",
        )
    with col3:
        st.metric(
            label="Duplicates " + ("Eliminated" if data_source == "clean" else "Detected"),
            value=f"{dups_eliminated:,}",
        )

    st.markdown("---")

    # --- Anomaly Distribution by Regional Office ---
    st.subheader("Anomaly Distribution by Regional Branch")

    if "Regional_Office" in df.columns and "Identity_Status" in df.columns:
        # Pre-aggregate to stay within Altair row limits
        agg = df.groupby("Regional_Office").agg(
            total=("Regional_Office", "size"),
            unverified=("Identity_Status", lambda x: (x == "UNVERIFIED_HOLDER").sum()),
        ).reset_index()
        agg["unverified_pct"] = (agg["unverified"] / agg["total"] * 100).round(1)

        if len(agg) > 0:
            chart = alt.Chart(agg).mark_bar().encode(
                x=alt.X("Regional_Office:N", sort="-y", title="Regional Office"),
                y=alt.Y("unverified:Q", title="Unverified Records"),
                color=alt.Color(
                    "unverified_pct:Q",
                    scale=alt.Scale(scheme="reds"),
                    title="Unverified %",
                ),
                tooltip=[
                    alt.Tooltip("Regional_Office:N", title="Office"),
                    alt.Tooltip("total:Q", title="Total Records", format=","),
                    alt.Tooltip("unverified:Q", title="Unverified", format=","),
                    alt.Tooltip("unverified_pct:Q", title="Unverified %", format=".1f"),
                ],
            ).properties(
                height=400,
            ).interactive()

            st.altair_chart(chart, use_container_width=True)
        else:
            st.info("No data available for charting.")
    else:
        st.info("Required columns (Regional_Office, Identity_Status) not found in dataset.")


def render_view2_revenue_assurance(df, data_source):
    """
    View 2: Revenue Assurance & Leakage Map

    Provides Albert and leadership with a monitoring view for revenue
    protection, including total valid revenue, flagged transactions,
    channel distribution, and an alert log.

    Parameters:
        df:          The active DataFrame (raw merged or clean).
        data_source: 'raw' or 'clean'.
    """
    st.header("View 2: Revenue Assurance & Leakage Map")
    st.markdown("---")

    # Determine the correct amount column name
    amount_col = None
    for candidate in ["Latest_Amount_Paid_GHS", "Amount_Paid_GHS"]:
        if candidate in df.columns:
            amount_col = candidate
            break

    channel_col = None
    for candidate in ["Latest_Payment_Channel", "Payment_Channel"]:
        if candidate in df.columns:
            channel_col = candidate
            break

    if amount_col is None:
        st.warning("No payment amount column found in the dataset.")
        return

    # --- KPI Metrics ---
    valid_mask = df[amount_col] > 0
    total_valid_revenue = df.loc[valid_mask, amount_col].sum()

    flagged_count = 0
    if "Revenue_Flag" in df.columns:
        flagged_count = (df["Revenue_Flag"] != "CLEAN").sum()
    else:
        flagged_count = (~valid_mask).sum()

    total_transactions = df[amount_col].notna().sum()
    protected_pct = ((total_transactions - flagged_count) / total_transactions * 100) if total_transactions > 0 else 0

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(
            label="Total Valid Revenue (GHS)",
            value=f"GHS {total_valid_revenue:,.2f}",
        )
    with col2:
        st.metric(
            label="Flagged Transactions",
            value=f"{flagged_count:,}",
        )
    with col3:
        st.metric(
            label="Revenue Protection Rate",
            value=f"{protected_pct:.1f}%",
        )

    st.markdown("---")

    # --- Payment Channel Distribution ---
    if channel_col is not None:
        st.subheader("Payment Channel Distribution")
        channel_agg = df[channel_col].value_counts().reset_index()
        channel_agg.columns = ["Channel", "Count"]

        if len(channel_agg) > 0:
            chart = alt.Chart(channel_agg).mark_arc(innerRadius=50).encode(
                theta=alt.Theta("Count:Q"),
                color=alt.Color(
                    "Channel:N",
                    scale=alt.Scale(scheme="tableau10"),
                    title="Payment Channel",
                ),
                tooltip=[
                    alt.Tooltip("Channel:N", title="Channel"),
                    alt.Tooltip("Count:Q", title="Transactions", format=","),
                ],
            ).properties(
                height=350,
                title="Transaction Volume by Payment Channel",
            )
            st.altair_chart(chart, use_container_width=True)

    st.markdown("---")

    # --- Alert Log: Flagged Transactions ---
    st.subheader("Alert Log: Revenue Anomalies for Strategic Review")

    if "Revenue_Flag" in df.columns:
        flagged_df = df[df["Revenue_Flag"] != "CLEAN"].copy()
    else:
        flagged_df = df[df[amount_col] <= 0].copy()

    if len(flagged_df) > 0:
        # Select relevant columns for the alert table
        display_cols = []
        for col in ["Registration_ID", "Revenue_Flag", amount_col, channel_col,
                     "Latest_Transaction_ID", "Transaction_ID", "Owner_Name", "Regional_Office"]:
            if col is not None and col in flagged_df.columns:
                display_cols.append(col)

        st.dataframe(
            flagged_df[display_cols].head(500),
            use_container_width=True,
            height=400,
        )
        st.caption(f"Showing top 500 of {len(flagged_df):,} flagged records.")
    else:
        st.success("No revenue anomalies detected in this dataset.")


def render_view3_zonal_metrics(df, data_source):
    """
    View 3: 2026 Zonal Registration Metrics

    Renders an interactive bar chart mapping vehicle concentrations across
    the new 2026 Zonal Area Codes.

    Parameters:
        df:          The active DataFrame.
        data_source: 'raw' or 'clean'.
    """
    st.header("View 3: 2026 Zonal Registration Metrics")
    st.markdown("---")

    if "Zonal_Area_Code" not in df.columns:
        if data_source == "raw":
            st.info(
                "**Zonal Area Codes are not available in the raw data.**\n\n"
                "The `Zonal_Area_Code` column is created during Lab 2 when students perform "
                "a broadcast join to map regional offices to the 2026 Zonal Area Codes.\n\n"
                "Switch to **Clean Transformed Data** to see this view, or complete Lab 2 first."
            )
        else:
            st.warning("The `Zonal_Area_Code` column is missing from the clean dataset. "
                       "Please verify Lab 2 was completed correctly.")
        return

    # --- Pre-aggregate by Zonal Area Code ---
    zonal_agg = df.groupby("Zonal_Area_Code").agg(
        vehicle_count=("Registration_ID", "nunique" if "Registration_ID" in df.columns else "size"),
    ).reset_index()

    # Add optional metrics if columns exist
    if "Identity_Status" in df.columns:
        verified_agg = df.groupby("Zonal_Area_Code")["Identity_Status"].apply(
            lambda x: (x == "VERIFIED").sum()
        ).reset_index()
        verified_agg.columns = ["Zonal_Area_Code", "verified_count"]
        zonal_agg = zonal_agg.merge(verified_agg, on="Zonal_Area_Code", how="left")
        zonal_agg["verified_pct"] = (
            zonal_agg["verified_count"] / zonal_agg["vehicle_count"] * 100
        ).round(1)

    amount_col = None
    for candidate in ["Latest_Amount_Paid_GHS", "Amount_Paid_GHS"]:
        if candidate in df.columns:
            amount_col = candidate
            break

    if amount_col is not None:
        avg_payment = df.groupby("Zonal_Area_Code")[amount_col].mean().reset_index()
        avg_payment.columns = ["Zonal_Area_Code", "avg_payment"]
        avg_payment["avg_payment"] = avg_payment["avg_payment"].round(2)
        zonal_agg = zonal_agg.merge(avg_payment, on="Zonal_Area_Code", how="left")

    # Sort by vehicle count descending
    zonal_agg = zonal_agg.sort_values("vehicle_count", ascending=False)

    # --- Bar Chart ---
    st.subheader("Vehicle Distribution Across 2026 Zonal Area Codes")

    if len(zonal_agg) > 0:
        tooltips = [
            alt.Tooltip("Zonal_Area_Code:N", title="Zone Code"),
            alt.Tooltip("vehicle_count:Q", title="Vehicles", format=","),
        ]
        if "verified_pct" in zonal_agg.columns:
            tooltips.append(alt.Tooltip("verified_pct:Q", title="Verified %", format=".1f"))
        if "avg_payment" in zonal_agg.columns:
            tooltips.append(alt.Tooltip("avg_payment:Q", title="Avg Payment (GHS)", format=",.2f"))

        chart = alt.Chart(zonal_agg).mark_bar().encode(
            x=alt.X("Zonal_Area_Code:N", sort="-y", title="2026 Zonal Area Code"),
            y=alt.Y("vehicle_count:Q", title="Number of Vehicles"),
            color=alt.Color(
                "Zonal_Area_Code:N",
                scale=alt.Scale(scheme="tableau20"),
                legend=None,
            ),
            tooltip=tooltips,
        ).properties(
            height=450,
        ).interactive()

        st.altair_chart(chart, use_container_width=True)
    else:
        st.info("No zonal data available for charting.")

    st.markdown("---")

    # --- Summary Table ---
    st.subheader("Zone-Level Summary Statistics")
    if len(zonal_agg) > 0:
        st.dataframe(
            zonal_agg.reset_index(drop=True),
            use_container_width=True,
            height=400,
        )


# =============================================================================
# SIDEBAR CONTROLS
# =============================================================================

def render_sidebar():
    """
    Render the sidebar controls for workspace selection, data source toggle,
    and view selection.

    Returns:
        Tuple of (selected_workspace_key, data_source, selected_view).
    """
    st.sidebar.title("DVLA Big Data Lab")
    st.sidebar.markdown("**Dashboard Controls**")
    st.sidebar.markdown("---")

    # --- Dropdown A: Workspace Selector ---
    workspace_key = st.sidebar.selectbox(
        "Select Workspace",
        options=list(WORKSPACES.keys()),
        format_func=lambda k: WORKSPACES[k],
        index=0,
        help="Choose which participant's data to visualize.",
    )

    st.sidebar.markdown("---")

    # --- Data Source Toggle ---
    data_source = st.sidebar.radio(
        "Data Source",
        options=["raw", "clean"],
        format_func=lambda x: "Raw Legacy Data" if x == "raw" else "Clean Transformed Data",
        index=0,
        help="Toggle between pre-ETL (raw) and post-ETL (clean) data views.",
    )

    st.sidebar.markdown("---")

    # --- Dropdown B: View Selector ---
    view_options = [
        "View 1: Data Cleansing & Quality Audit",
        "View 2: Revenue Assurance & Leakage Map",
        "View 3: 2026 Zonal Registration Metrics",
    ]
    selected_view = st.sidebar.selectbox(
        "Select Dashboard View",
        options=view_options,
        index=0,
        help="Choose the analytical perspective to display.",
    )

    st.sidebar.markdown("---")

    # --- Sidebar Info ---
    st.sidebar.markdown(
        "**Lab Info**\n\n"
        "- DVLA Ghana RBDI Department\n"
        "- Director: Abraham Zaato\n"
        "- Big Data Training Lab, June 2026\n"
    )

    return workspace_key, data_source, selected_view


# =============================================================================
# MAIN APPLICATION
# =============================================================================

def main():
    """
    Main entry point for the Streamlit dashboard application.

    Orchestrates sidebar controls, data loading, and view rendering
    with comprehensive error handling.
    """
    # --- Render sidebar and get user selections ---
    workspace_key, data_source, selected_view = render_sidebar()

    # --- Page Header ---
    st.title("DVLA Ghana - Big Data Lab Dashboard")
    st.markdown(
        f"**Workspace:** {WORKSPACES[workspace_key]} | "
        f"**Data Source:** {'Raw Legacy Data' if data_source == 'raw' else 'Clean Transformed Data'}"
    )
    st.markdown("---")

    # --- Load Data ---
    df = None
    raw_registry = None

    if data_source == "raw":
        merged, registry, payments = load_raw_data()
        if merged is None:
            st.error(
                "**Raw data files not found!**\n\n"
                "The files `raw_data/legacy_vehicle_registry.csv` and "
                "`raw_data/payment_transaction_log.csv` do not exist.\n\n"
                "Please run `python generate_dvla_data.py` first to generate the datasets."
            )
            return
        df = merged
        raw_registry = registry

    else:  # clean
        df = load_clean_data(workspace_key)
        if df is None:
            st.warning(
                f"**Clean data not yet available for {WORKSPACES[workspace_key]}.**\n\n"
                f"The file `./{workspace_key}/output/powerbi_ready.csv` does not exist.\n\n"
                "To generate this file:\n"
                "1. Open **Lab 2: PySpark ETL & Transformation** in JupyterLab.\n"
                "2. Complete all steps through Step 13 (Export as Flat CSV).\n"
                "3. Return to this dashboard and refresh the page."
            )
            return

        # Also load raw registry for comparison metrics
        _, raw_registry, _ = load_raw_data()

    # --- Guard against empty DataFrames ---
    if df is None or len(df) == 0:
        st.warning("The loaded dataset is empty. Please verify your data files.")
        return

    # --- Render Selected View ---
    if "View 1" in selected_view:
        render_view1_quality_audit(df, data_source, raw_registry)
    elif "View 2" in selected_view:
        render_view2_revenue_assurance(df, data_source)
    elif "View 3" in selected_view:
        render_view3_zonal_metrics(df, data_source)


if __name__ == "__main__":
    main()
