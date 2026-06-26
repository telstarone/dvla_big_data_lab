#!/usr/bin/env python3
# =============================================================================
# generate_dvla_data.py
# =============================================================================
# DVLA Ghana Big Data Practical Lab — Comprehensive Data Generation Engine
#
# Purpose:
#   Generates two large, realistic relational datasets modelling the Driver and
#   Vehicle Licensing Authority (DVLA) Ghana's legacy vehicle registration
#   system and payment transaction logs. Both datasets are intentionally
#   injected with data-quality anomalies (duplicates, nulls, mixed formats,
#   orphan records, revenue leakage) to serve as cleanup targets during the
#   hands-on ETL lab exercises.
#
# Output:
#   raw_data/legacy_vehicle_registry.csv   (~52,500 rows)
#   raw_data/payment_transaction_log.csv   (~55,000 rows)
#
# Usage:
#   python generate_dvla_data.py
#
# Author:  Lab Infrastructure (auto-generated)
# Date:    June 2026
# =============================================================================

import os
import random
import string
import datetime

import numpy as np
import pandas as pd


# =============================================================================
# CONFIGURATION — Deterministic Seed for Reproducibility
# =============================================================================
# Setting a fixed seed ensures every run produces identical datasets.
# This is critical so all four workspaces (kevin, benjamin, albert, peter)
# operate on the exact same source data.
SEED = 2026
random.seed(SEED)
np.random.seed(SEED)

# Number of unique base records before anomaly injection
BASE_VEHICLE_ROWS = 50_000
BASE_PAYMENT_ROWS = 50_000

# Anomaly injection rates
DUPLICATE_RATE_VEHICLES = 0.05      # 5% exact duplicate rows
NULL_ID_RATE = 0.10                 # 10% null National_ID_Number
MIXED_DATE_FORMAT_RATE = 0.30       # 30% dates reformatted to DD/MM/YYYY
ORPHAN_PAYMENT_RATE = 0.10          # 10% payments with non-existent Registration_IDs
ZERO_NEGATIVE_AMOUNT_RATE = 0.05    # 5% payments with amount <= 0
DUPLICATE_RATE_PAYMENTS = 0.05      # 5% exact duplicate payment rows

# Output directory (relative to script location)
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "raw_data")


# =============================================================================
# REFERENCE DATA — Realistic Ghanaian Domain Values
# =============================================================================

# DVLA Ghana regional branch offices (20 branches mapped to Zonal dictionary)
REGIONAL_OFFICES = [
    "Accra Metro", "Weija", "Madina", "Tema",           # Greater Accra
    "Kumasi", "Obuasi", "Mampong",                       # Ashanti
    "Tamale",                                             # Northern
    "Takoradi", "Tarkwa",                                 # Western
    "Cape Coast", "Winneba",                              # Central
    "Koforidua", "Nkawkaw",                               # Eastern
    "Sunyani", "Techiman",                                # Bono
    "Bolgatanga",                                         # Upper East
    "Wa",                                                 # Upper West
    "Ho", "Aflao",                                        # Volta
]

# Weighted distribution: Greater Accra offices get more registrations (realistic)
REGIONAL_WEIGHTS = [
    0.15, 0.06, 0.07, 0.10,    # Accra Metro, Weija, Madina, Tema
    0.10, 0.03, 0.02,           # Kumasi, Obuasi, Mampong
    0.05,                        # Tamale
    0.04, 0.02,                  # Takoradi, Tarkwa
    0.03, 0.02,                  # Cape Coast, Winneba
    0.04, 0.02,                  # Koforidua, Nkawkaw
    0.03, 0.02,                  # Sunyani, Techiman
    0.03,                        # Bolgatanga
    0.02,                        # Wa
    0.03, 0.02,                  # Ho, Aflao
]

# Vehicle makes common on Ghanaian roads (weighted toward Toyota dominance)
VEHICLE_MAKES = [
    "Toyota", "Hyundai", "Nissan", "Honda", "Kia",
    "Mercedes-Benz", "Ford", "Volkswagen", "Suzuki", "Mitsubishi",
    "BMW", "Peugeot", "Renault", "Isuzu", "Mahindra",
]
VEHICLE_MAKE_WEIGHTS = [
    0.25, 0.12, 0.12, 0.08, 0.08,
    0.05, 0.05, 0.04, 0.04, 0.04,
    0.03, 0.03, 0.02, 0.03, 0.02,
]

# Ghanaian given names and surnames for realistic Owner_Name generation
GHANAIAN_FIRST_NAMES = [
    "Kwame", "Kwesi", "Kofi", "Yaw", "Kwaku", "Kwabena", "Kojo",
    "Ama", "Akua", "Abena", "Afia", "Adwoa", "Akosua", "Yaa",
    "Nana", "Esi", "Efua", "Adjoa", "Ekua", "Afua",
    "Emmanuel", "Samuel", "Daniel", "Michael", "Joseph",
    "Grace", "Mercy", "Priscilla", "Beatrice", "Comfort",
    "Isaac", "Abraham", "Benjamin", "Albert", "Peter",
    "Felicia", "Rita", "Patricia", "Elizabeth", "Dorothy",
    "Francis", "George", "James", "David", "Charles",
    "Agnes", "Cecilia", "Victoria", "Millicent", "Naomi",
]

GHANAIAN_SURNAMES = [
    "Mensah", "Asante", "Boateng", "Osei", "Agyemang",
    "Owusu", "Amoah", "Darko", "Appiah", "Baffoe",
    "Quaye", "Nartey", "Tetteh", "Lartey", "Adjei",
    "Annan", "Bonsu", "Gyasi", "Frimpong", "Acheampong",
    "Amponsah", "Ofori", "Sarpong", "Wiredu", "Addo",
    "Asamoah", "Opoku", "Yeboah", "Addai", "Danso",
    "Acquah", "Adomako", "Baah", "Doku", "Ampofo",
    "Gyamfi", "Kumi", "Tawiah", "Nkrumah", "Adu",
    "Dzamesi", "Wotorgbui", "Zaato", "Djameshie", "Peh",
    "Agbenyega", "Amediku", "Dogbe", "Kpodo", "Amegatcher",
]

# Payment channels used at DVLA Ghana
PAYMENT_CHANNELS = [
    "MTN MoMo", "Telecel Cash", "AT Money", "e-Levy Portal", "Bank Branch",
]
PAYMENT_CHANNEL_WEIGHTS = [0.35, 0.15, 0.10, 0.20, 0.20]

# Ghana vehicle registration plate prefix codes (region-based)
PLATE_PREFIXES = [
    "GR", "GW", "GN", "GS", "GE", "GT", "GC", "GA", "GB", "GX",
    "AS", "BA", "WR", "CR", "ER", "NR", "UE", "UW", "VR",
]


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def generate_registration_id(index: int) -> str:
    """
    Generate a Ghanaian-style vehicle registration ID.

    Format: PREFIX-NNNN-YY  (e.g., GR-1234-24)
    - PREFIX: Regional code (2 letters)
    - NNNN:   Sequential/random 4-digit number
    - YY:     Year suffix (15-25 for 2015-2025)

    Parameters:
        index: Row index used to ensure uniqueness.

    Returns:
        A formatted registration ID string.
    """
    prefix = random.choice(PLATE_PREFIXES)
    number = (index % 9999) + 1  # 1-9999
    year_suffix = random.randint(15, 25)
    return f"{prefix}-{number:04d}-{year_suffix:02d}"


def generate_chassis_number() -> str:
    """
    Generate a realistic 17-character Vehicle Identification Number (VIN).

    A VIN consists of uppercase letters (excluding I, O, Q to avoid confusion
    with 1, 0) and digits. This is the international standard used by DVLA
    for vehicle identification.

    Returns:
        A 17-character alphanumeric VIN string.
    """
    # Valid VIN characters (no I, O, Q)
    valid_chars = "ABCDEFGHJKLMNPRSTUVWXYZ0123456789"
    return "".join(random.choice(valid_chars) for _ in range(17))


def generate_owner_name() -> str:
    """
    Generate a realistic Ghanaian full name by combining random first
    and last names from curated pools of Akan, Ewe, Ga, and Dagbani names.

    Returns:
        A full name string (e.g., "Kwame Mensah").
    """
    first = random.choice(GHANAIAN_FIRST_NAMES)
    last = random.choice(GHANAIAN_SURNAMES)
    return f"{first} {last}"


def generate_ghana_card_id() -> str:
    """
    Generate a Ghana Card (National Identification) number.

    Format: GHA-NNNNNNNNN-N  (e.g., GHA-012345678-9)
    - GHA:         Country prefix
    - NNNNNNNNN:   9-digit unique identifier
    - N:           Check digit

    This is the format used by the National Identification Authority (NIA)
    of Ghana for the Ghana Card biometric ID system.

    Returns:
        A formatted Ghana Card ID string.
    """
    digits = "".join([str(random.randint(0, 9)) for _ in range(9)])
    check = str(random.randint(0, 9))
    return f"GHA-{digits}-{check}"


def generate_registration_date() -> str:
    """
    Generate a random registration date between 2015-01-01 and 2025-12-31
    in the standard YYYY-MM-DD format.

    This format will later be partially corrupted (30% converted to DD/MM/YYYY)
    to simulate the legacy data inconsistencies found in DVLA's historical
    records after multiple system migrations.

    Returns:
        A date string in YYYY-MM-DD format.
    """
    start_date = datetime.date(2015, 1, 1)
    end_date = datetime.date(2025, 12, 31)
    delta = (end_date - start_date).days
    random_date = start_date + datetime.timedelta(days=random.randint(0, delta))
    return random_date.strftime("%Y-%m-%d")


def generate_payment_timestamp() -> str:
    """
    Generate a random payment timestamp between 2020-01-01 and 2025-12-31
    in ISO 8601 format (YYYY-MM-DD HH:MM:SS).

    Payment records span a narrower window than registrations because the
    digital payment infrastructure was deployed more recently.

    Returns:
        A datetime string in ISO 8601 format.
    """
    start_dt = datetime.datetime(2020, 1, 1, 8, 0, 0)
    end_dt = datetime.datetime(2025, 12, 31, 17, 0, 0)
    delta_seconds = int((end_dt - start_dt).total_seconds())
    random_dt = start_dt + datetime.timedelta(seconds=random.randint(0, delta_seconds))
    return random_dt.strftime("%Y-%m-%d %H:%M:%S")


# =============================================================================
# DATASET 1: LEGACY VEHICLE REGISTRY
# =============================================================================

def generate_vehicle_registry() -> pd.DataFrame:
    """
    Generate the legacy_vehicle_registry.csv dataset.

    This dataset models DVLA Ghana's historical vehicle registration records.
    It contains 50,000 base records with the following intentional anomalies
    injected to serve as cleanup targets during the ETL lab:

    Anomalies:
      - 5% exact duplicate rows (~2,500 rows)
      - 10% null National_ID_Number values (~5,000 entries)
      - 30% mixed date format (DD/MM/YYYY instead of YYYY-MM-DD)

    Returns:
        A pandas DataFrame containing the vehicle registry with anomalies.
    """
    print("[1/6] Generating base vehicle registry records...")

    # --- Step 1: Generate unique Registration_IDs ---
    # We use a set to guarantee uniqueness before building the DataFrame.
    reg_ids = set()
    while len(reg_ids) < BASE_VEHICLE_ROWS:
        reg_ids.add(generate_registration_id(len(reg_ids) + random.randint(0, 100000)))
    reg_ids = list(reg_ids)[:BASE_VEHICLE_ROWS]

    # --- Step 2: Generate all column values ---
    data = {
        "Registration_ID": reg_ids,
        "Chassis_Number": [generate_chassis_number() for _ in range(BASE_VEHICLE_ROWS)],
        "Owner_Name": [generate_owner_name() for _ in range(BASE_VEHICLE_ROWS)],
        "National_ID_Number": [generate_ghana_card_id() for _ in range(BASE_VEHICLE_ROWS)],
        "Registration_Date": [generate_registration_date() for _ in range(BASE_VEHICLE_ROWS)],
        "Vehicle_Make": random.choices(VEHICLE_MAKES, weights=VEHICLE_MAKE_WEIGHTS, k=BASE_VEHICLE_ROWS),
        "Regional_Office": random.choices(REGIONAL_OFFICES, weights=REGIONAL_WEIGHTS, k=BASE_VEHICLE_ROWS),
    }

    df = pd.DataFrame(data)

    # --- Step 3: Inject 10% null National_ID_Number ---
    # In real DVLA data, missing identity records occur when vehicle owners
    # registered before the Ghana Card system was deployed, or when manual
    # entry clerks skipped the field.
    print("[2/6] Injecting 10% null National_ID_Number values...")
    null_count = int(BASE_VEHICLE_ROWS * NULL_ID_RATE)
    null_indices = np.random.choice(df.index, size=null_count, replace=False)
    df.loc[null_indices, "National_ID_Number"] = np.nan

    # --- Step 4: Inject 30% mixed date formats ---
    # Legacy DVLA systems used DD/MM/YYYY while modern systems use YYYY-MM-DD.
    # This inconsistency is a common real-world data migration challenge.
    print("[3/6] Injecting 30% mixed date formats (DD/MM/YYYY)...")
    mixed_count = int(BASE_VEHICLE_ROWS * MIXED_DATE_FORMAT_RATE)
    mixed_indices = np.random.choice(df.index, size=mixed_count, replace=False)
    for idx in mixed_indices:
        original_date = df.at[idx, "Registration_Date"]
        try:
            parsed = datetime.datetime.strptime(original_date, "%Y-%m-%d")
            df.at[idx, "Registration_Date"] = parsed.strftime("%d/%m/%Y")
        except (ValueError, TypeError):
            pass  # Skip if already converted or malformed

    # --- Step 5: Inject 5% exact duplicate rows ---
    # Duplicates occur when the same vehicle is registered multiple times
    # due to system glitches, double submissions at branch offices, or
    # paper-to-digital migration errors.
    print("[4/6] Injecting 5% exact duplicate rows...")
    dup_count = int(BASE_VEHICLE_ROWS * DUPLICATE_RATE_VEHICLES)
    dup_indices = np.random.choice(df.index, size=dup_count, replace=False)
    duplicates = df.loc[dup_indices].copy()
    df = pd.concat([df, duplicates], ignore_index=True)

    # --- Step 6: Shuffle to distribute anomalies naturally ---
    df = df.sample(frac=1, random_state=SEED).reset_index(drop=True)

    return df


# =============================================================================
# DATASET 2: PAYMENT TRANSACTION LOG
# =============================================================================

def generate_payment_transactions(valid_reg_ids: list) -> pd.DataFrame:
    """
    Generate the payment_transaction_log.csv dataset.

    This dataset models DVLA Ghana's digital payment records for vehicle
    registration and renewal fees. It is relationally linked to the vehicle
    registry via Registration_ID.

    Anomalies injected (revenue leakage indicators):
      - 10% orphan payments (Registration_ID not in vehicle registry)
      - 5% zero or negative payment amounts
      - 5% exact duplicate transaction rows

    Parameters:
        valid_reg_ids: List of Registration_IDs from the vehicle registry
                       (used to create valid linkages and orphan references).

    Returns:
        A pandas DataFrame containing payment transactions with anomalies.
    """
    print("[5/6] Generating base payment transaction records...")

    # --- Step 1: Generate Transaction_IDs ---
    txn_ids = [f"TXN-{i:08d}" for i in range(1, BASE_PAYMENT_ROWS + 1)]

    # --- Step 2: Assign Registration_IDs ---
    # 90% of payments reference valid vehicle registrations.
    # 10% are "orphan" payments — they reference Registration_IDs that
    # do not exist in the vehicle registry. In DVLA operations, this can
    # happen when a payment is processed for a vehicle that was never
    # formally registered, or when data entry errors create broken links.
    valid_count = int(BASE_PAYMENT_ROWS * (1 - ORPHAN_PAYMENT_RATE))
    orphan_count = BASE_PAYMENT_ROWS - valid_count

    # Valid payments reference existing Registration_IDs
    valid_payment_reg_ids = random.choices(valid_reg_ids, k=valid_count)

    # Orphan payments reference fabricated Registration_IDs
    orphan_reg_ids = [f"ORPHAN-{random.randint(90000, 99999):05d}-XX" for _ in range(orphan_count)]

    all_reg_ids = valid_payment_reg_ids + orphan_reg_ids
    random.shuffle(all_reg_ids)

    # --- Step 3: Generate payment amounts ---
    # Vehicle registration/renewal fees in Ghana typically range from
    # GHS 50 (motorcycle renewals) to GHS 5,000 (commercial vehicles).
    # We use a normal distribution centered around GHS 350 (standard saloon).
    amounts = np.random.normal(loc=350, scale=150, size=BASE_PAYMENT_ROWS)
    amounts = np.clip(amounts, 50, 5000)  # Clamp to realistic range
    amounts = np.round(amounts, 2)

    # --- Step 4: Inject 5% zero/negative amounts ---
    # Revenue leakage: payments with zero or negative values indicate
    # system errors, unauthorized refund entries, or data corruption.
    # These must be flagged during the ETL process as revenue risks.
    zero_neg_count = int(BASE_PAYMENT_ROWS * ZERO_NEGATIVE_AMOUNT_RATE)
    zero_neg_indices = np.random.choice(range(BASE_PAYMENT_ROWS), size=zero_neg_count, replace=False)
    for idx in zero_neg_indices:
        # 50/50 split between zero and negative values
        if random.random() < 0.5:
            amounts[idx] = 0.0
        else:
            amounts[idx] = -round(random.uniform(10, 500), 2)

    # --- Step 5: Build the DataFrame ---
    data = {
        "Transaction_ID": txn_ids,
        "Registration_ID": all_reg_ids,
        "Amount_Paid_GHS": amounts,
        "Payment_Timestamp": [generate_payment_timestamp() for _ in range(BASE_PAYMENT_ROWS)],
        "Payment_Channel": random.choices(
            PAYMENT_CHANNELS, weights=PAYMENT_CHANNEL_WEIGHTS, k=BASE_PAYMENT_ROWS
        ),
    }

    df = pd.DataFrame(data)

    # --- Step 6: Inject 5% exact duplicate transactions ---
    # Duplicate payment entries occur when the payment gateway retries
    # a timed-out request, or when branch operators accidentally submit
    # the same transaction form twice.
    print("[6/6] Injecting 5% duplicate payment transactions...")
    dup_count = int(BASE_PAYMENT_ROWS * DUPLICATE_RATE_PAYMENTS)
    dup_indices = np.random.choice(df.index, size=dup_count, replace=False)
    duplicates = df.loc[dup_indices].copy()
    df = pd.concat([df, duplicates], ignore_index=True)

    # Shuffle to distribute anomalies naturally
    df = df.sample(frac=1, random_state=SEED).reset_index(drop=True)

    return df


# =============================================================================
# MAIN EXECUTION
# =============================================================================

def main():
    """
    Main entry point. Generates both datasets, saves them to raw_data/,
    and prints a summary report of injected anomalies for verification.
    """
    print("=" * 70)
    print("  DVLA Ghana Big Data Lab -- Data Generation Engine")
    print("  Generating realistic datasets with intentional anomalies")
    print("=" * 70)

    # --- Create output directory ---
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"\nOutput directory: {OUTPUT_DIR}\n")

    # --- Generate Dataset 1: Vehicle Registry ---
    registry_df = generate_vehicle_registry()
    registry_path = os.path.join(OUTPUT_DIR, "legacy_vehicle_registry.csv")
    registry_df.to_csv(registry_path, index=False, encoding="utf-8")
    print(f"  [OK] Saved: {registry_path}")

    # --- Generate Dataset 2: Payment Transactions ---
    # Extract the unique valid Registration_IDs from the base records
    # (before duplicates were injected) for creating orphan references.
    unique_reg_ids = registry_df["Registration_ID"].unique().tolist()
    payments_df = generate_payment_transactions(unique_reg_ids)
    payments_path = os.path.join(OUTPUT_DIR, "payment_transaction_log.csv")
    payments_df.to_csv(payments_path, index=False, encoding="utf-8")
    print(f"  [OK] Saved: {payments_path}")

    # --- Print Verification Summary ---
    print("\n" + "=" * 70)
    print("  DATA GENERATION SUMMARY REPORT")
    print("=" * 70)

    # Vehicle Registry Stats
    total_reg = len(registry_df)
    null_ids = registry_df["National_ID_Number"].isna().sum()
    unique_reg = registry_df.drop_duplicates().shape[0]
    dup_reg = total_reg - unique_reg

    print(f"\n  [REGISTRY] legacy_vehicle_registry.csv:")
    print(f"     Total rows:              {total_reg:,}")
    print(f"     Unique rows:             {unique_reg:,}")
    print(f"     Duplicate rows:          {dup_reg:,} ({dup_reg/total_reg*100:.1f}%)")
    print(f"     Null National_ID:        {null_ids:,} ({null_ids/total_reg*100:.1f}%)")

    # Count mixed date formats (DD/MM/YYYY pattern)
    mixed_dates = registry_df["Registration_Date"].str.match(r"^\d{2}/\d{2}/\d{4}$").sum()
    print(f"     Mixed date format:       {mixed_dates:,} ({mixed_dates/total_reg*100:.1f}%)")

    # Payment Transaction Stats
    total_pay = len(payments_df)
    orphans = payments_df[payments_df["Registration_ID"].str.startswith("ORPHAN-")].shape[0]
    zero_neg = payments_df[payments_df["Amount_Paid_GHS"] <= 0].shape[0]
    unique_pay = payments_df.drop_duplicates().shape[0]
    dup_pay = total_pay - unique_pay

    print(f"\n  [PAYMENTS] payment_transaction_log.csv:")
    print(f"     Total rows:              {total_pay:,}")
    print(f"     Unique rows:             {unique_pay:,}")
    print(f"     Duplicate rows:          {dup_pay:,} ({dup_pay/total_pay*100:.1f}%)")
    print(f"     Orphan payments:         {orphans:,} ({orphans/total_pay*100:.1f}%)")
    print(f"     Zero/negative amounts:   {zero_neg:,} ({zero_neg/total_pay*100:.1f}%)")

    print(f"\n  [DONE] Data generation complete. Files ready in: {OUTPUT_DIR}")
    print("=" * 70)


if __name__ == "__main__":
    main()
