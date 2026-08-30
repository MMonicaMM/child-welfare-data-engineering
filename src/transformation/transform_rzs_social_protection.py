from pathlib import Path

import pandas as pd


# --------------------------------------------------
# Configuration
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_FILE = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "rzs"
    / "children_social_protection.xlsx"
)

SOURCE_ID = "SRC001"


# --------------------------------------------------
# Load
# --------------------------------------------------

def load_raw_data() -> pd.DataFrame:
    """Load the raw RZS Excel dataset."""

    print("Loading raw dataset...")

    df = pd.read_excel(
        RAW_FILE,
        sheet_name="Деца и омладина"
    )

    print(f"Loaded {len(df)} rows.")

    return df


# --------------------------------------------------
# Rename columns
# --------------------------------------------------

def standardize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """Rename source columns to standardized English names."""

    df = df.rename(
        columns={
            "Град/Општина": "municipality",
            "Матични број општине": "municipality_code",
            "Година": "year",
            "Категорије": "category",
            "Број": "value",
        }
    )

    return df


# --------------------------------------------------
# Clean text
# --------------------------------------------------

def clean_text_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Clean whitespace from text columns."""

    df["municipality"] = (
        df["municipality"]
        .astype(str)
        .str.strip()
    )

    df["category"] = (
        df["category"]
        .astype(str)
        .str.replace(r"\s+", " ", regex=True)
        .str.strip()
    )

    return df


# --------------------------------------------------
# Standardize data types
# --------------------------------------------------

def standardize_data_types(df: pd.DataFrame) -> pd.DataFrame:
    """Convert columns to expected data types."""

    df["municipality_code"] = df["municipality_code"].astype(int)

    df["year"] = df["year"].astype(int)

    df["value"] = df["value"].astype(int)

    return df


# --------------------------------------------------
# Validation
# --------------------------------------------------

def validate_data(df: pd.DataFrame) -> None:
    """Validate transformed dataset."""

    required_columns = {
        "municipality",
        "municipality_code",
        "year",
        "category",
        "value",
    }

    missing_columns = required_columns - set(df.columns)

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    if df.isnull().any().any():
        raise ValueError(
            "Dataset contains missing values."
        )

    if (df["value"] < 0).any():
        raise ValueError(
            "Dataset contains negative values."
        )

    if not df["year"].between(1900, 2100).all():
        raise ValueError(
            "Dataset contains invalid years."
        )

    if df.duplicated().any():
        raise ValueError(
            "Dataset contains duplicate rows."
        )

    print("Validation passed.")


# --------------------------------------------------
# Add metadata
# --------------------------------------------------

def add_metadata(df: pd.DataFrame) -> pd.DataFrame:
    """Add pipeline metadata."""

    df["source_id"] = SOURCE_ID

    df["loaded_at"] = pd.Timestamp.now()

    return df


# --------------------------------------------------
# Main transformation
# --------------------------------------------------

def transform() -> pd.DataFrame:

    df = load_raw_data()

    df = standardize_column_names(df)

    df = clean_text_columns(df)

    df = standardize_data_types(df)

    validate_data(df)

    df = add_metadata(df)

    return df


def main():

    df = transform()

    print("\n" + "=" * 60)
    print("TRANSFORMED DATASET")
    print("=" * 60)

    print(f"Rows: {len(df)}")
    print(f"Columns: {len(df.columns)}")

    print("\nColumns:")
    for column in df.columns:
        print(f" - {column}")

    print("\nFirst 5 rows:")
    print(df.head())

    print("\nTransformation completed successfully.")


if __name__ == "__main__":
    main()