from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_FILE = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "rzs"
    / "children_social_protection.xlsx"
)


def main():

    print("Loading dataset...")

    df = pd.read_excel(RAW_FILE)

    print("\n" + "=" * 60)
    print("DATASET OVERVIEW")
    print("=" * 60)

    print(f"Rows: {len(df)}")
    print(f"Columns: {len(df.columns)}")

    print("\nColumn names:")
    for column in df.columns:
        print(f" - {column}")

    print("\nData types:")
    print(df.dtypes)

    print("\nMissing values:")
    print(df.isnull().sum())

    print("\nDuplicate rows:")
    print(df.duplicated().sum())

    print("\n" + "=" * 60)
    print("YEARS")
    print("=" * 60)

    print(
        df["Година"]
        .value_counts()
        .sort_index()
    )

    print("\n" + "=" * 60)
    print("MUNICIPALITIES")
    print("=" * 60)

    print(
        df["Град/Општина"]
        .value_counts()
    )

    print("\n" + "=" * 60)
    print("CATEGORIES")
    print("=" * 60)

    categories = (
        df["Категорије"]
        .dropna()
        .unique()
    )

    for category in categories:
        print(f" - {category}")

    print("\n" + "=" * 60)
    print("NUMERIC SUMMARY")
    print("=" * 60)

    print(
        df["Број"].describe()
    )


if __name__ == "__main__":
    main()