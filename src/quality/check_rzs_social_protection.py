from pathlib import Path
import sys

from sqlalchemy import text


PROJECT_ROOT = Path(__file__).resolve().parents[2]

sys.path.append(str(PROJECT_ROOT))


from src.database.connection import get_database_engine


TABLE = "staging.rzs_social_protection"


def check_row_count(connection):

    result = connection.execute(
        text(f"SELECT COUNT(*) FROM {TABLE}")
    )

    count = result.scalar()

    if count == 0:
        raise ValueError("Dataset is empty.")

    print(f"✓ Row count: {count}")


def check_nulls(connection):

    query = text(
        f"""
        SELECT COUNT(*)
        FROM {TABLE}
        WHERE municipality IS NULL
           OR municipality_code IS NULL
           OR year IS NULL
           OR category IS NULL
           OR value IS NULL
           OR source_id IS NULL
        """
    )

    result = connection.execute(query)

    count = result.scalar()

    if count > 0:
        raise ValueError(
            f"Found {count} rows with NULL values."
        )

    print("✓ No NULL values")


def check_negative_values(connection):

    query = text(
        f"""
        SELECT COUNT(*)
        FROM {TABLE}
        WHERE value < 0
        """
    )

    result = connection.execute(query)

    count = result.scalar()

    if count > 0:
        raise ValueError(
            f"Found {count} negative values."
        )

    print("✓ No negative values")


def check_years(connection):

    query = text(
        f"""
        SELECT COUNT(*)
        FROM {TABLE}
        WHERE year < 1900
           OR year > 2100
        """
    )

    result = connection.execute(query)

    count = result.scalar()

    if count > 0:
        raise ValueError(
            f"Found {count} invalid years."
        )

    print("✓ Years are valid")


def check_duplicates(connection):

    query = text(
        f"""
        SELECT
            source_id,
            municipality_code,
            year,
            category,
            COUNT(*)
        FROM {TABLE}
        GROUP BY
            source_id,
            municipality_code,
            year,
            category
        HAVING COUNT(*) > 1
        """
    )

    result = connection.execute(query)

    duplicates = result.fetchall()

    if duplicates:
        raise ValueError(
            f"Found {len(duplicates)} duplicate keys."
        )

    print("✓ No duplicate business keys")


def main():

    print("=" * 60)
    print("DATA QUALITY CHECKS")
    print("=" * 60)

    engine = get_database_engine()

    with engine.connect() as connection:

        check_row_count(connection)
        check_nulls(connection)
        check_negative_values(connection)
        check_years(connection)
        check_duplicates(connection)

    print("\nAll data quality checks passed.")


if __name__ == "__main__":
    main()