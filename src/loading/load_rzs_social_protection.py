from pathlib import Path
import sys

from sqlalchemy import text


# --------------------------------------------------
# Add project root to Python path
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

sys.path.append(str(PROJECT_ROOT))


from src.database.connection import get_database_engine
from src.transformation.transform_rzs_social_protection import transform


# --------------------------------------------------
# Configuration
# --------------------------------------------------

TARGET_TABLE = "staging.rzs_social_protection"


# --------------------------------------------------
# Load data
# --------------------------------------------------

def load_to_postgres(df):

    engine = get_database_engine()

    print("Loading data into PostgreSQL...")

    df.to_sql(
        name="rzs_social_protection",
        con=engine,
        schema="staging",
        if_exists="append",
        index=False,
        method="multi",
    )

    print(f"Loaded {len(df)} rows into {TARGET_TABLE}.")


# --------------------------------------------------
# Verify load
# --------------------------------------------------

def verify_load():

    engine = get_database_engine()

    with engine.connect() as connection:

        result = connection.execute(
            text(
                """
                SELECT COUNT(*)
                FROM staging.rzs_social_protection
                """
            )
        )

        count = result.scalar()

    print(f"Rows currently in {TARGET_TABLE}: {count}")


# --------------------------------------------------
# Main
# --------------------------------------------------

def main():

    print("=" * 60)
    print("RZS SOCIAL PROTECTION LOAD")
    print("=" * 60)

    # Transform raw data
    df = transform()

    print(f"\nTransformed rows: {len(df)}")

    # Load into PostgreSQL
    load_to_postgres(df)

    # Verify
    verify_load()

    print("\nLoad completed successfully.")


if __name__ == "__main__":
    main()