from pathlib import Path
import sys

from sqlalchemy import text


# --------------------------------------------------
# Project root
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

sys.path.append(str(PROJECT_ROOT))


from src.database.connection import get_database_engine


# --------------------------------------------------
# Load dimensions
# --------------------------------------------------

def load_municipality_dimension(connection):

    print("Loading dim_municipality...")

    connection.execute(
        text(
            """
            INSERT INTO warehouse.dim_municipality (
                municipality_code,
                municipality_name
            )
            SELECT DISTINCT
                municipality_code,
                municipality
            FROM staging.rzs_social_protection
            ON CONFLICT (municipality_code)
            DO UPDATE SET
                municipality_name = EXCLUDED.municipality_name;
            """
        )
    )

    print("✓ Municipality dimension loaded.")


def load_category_dimension(connection):

    print("Loading dim_category...")

    connection.execute(
        text(
            """
            INSERT INTO warehouse.dim_category (
                category_name
            )
            SELECT DISTINCT
                category
            FROM staging.rzs_social_protection
            ON CONFLICT (category_name)
            DO NOTHING;
            """
        )
    )

    print("✓ Category dimension loaded.")


def load_year_dimension(connection):

    print("Loading dim_year...")

    connection.execute(
        text(
            """
            INSERT INTO warehouse.dim_year (
                year_key,
                year
            )
            SELECT DISTINCT
                year,
                year
            FROM staging.rzs_social_protection
            ON CONFLICT (year_key)
            DO NOTHING;
            """
        )
    )

    print("✓ Year dimension loaded.")


# --------------------------------------------------
# Load fact table
# --------------------------------------------------

def load_fact_table(connection):

    print("Loading fact_social_protection...")

    connection.execute(
        text(
            """
            INSERT INTO warehouse.fact_social_protection (
                municipality_key,
                category_key,
                year_key,
                value,
                source_id,
                loaded_at
            )
            SELECT
                m.municipality_key,
                c.category_key,
                y.year_key,
                s.value,
                s.source_id,
                s.loaded_at

            FROM staging.rzs_social_protection s

            JOIN warehouse.dim_municipality m
                ON m.municipality_code = s.municipality_code

            JOIN warehouse.dim_category c
                ON c.category_name = s.category

            JOIN warehouse.dim_year y
                ON y.year = s.year

            ON CONFLICT (
                municipality_key,
                category_key,
                year_key,
                source_id
            )
            DO UPDATE SET
                value = EXCLUDED.value,
                loaded_at = EXCLUDED.loaded_at;
            """
        )
    )

    print("✓ Fact table loaded.")


# --------------------------------------------------
# Verify warehouse
# --------------------------------------------------

def verify_warehouse(connection):

    print("\n" + "=" * 60)
    print("WAREHOUSE VERIFICATION")
    print("=" * 60)

    queries = {
        "Municipalities": """
            SELECT COUNT(*)
            FROM warehouse.dim_municipality
        """,

        "Categories": """
            SELECT COUNT(*)
            FROM warehouse.dim_category
        """,

        "Years": """
            SELECT COUNT(*)
            FROM warehouse.dim_year
        """,

        "Fact records": """
            SELECT COUNT(*)
            FROM warehouse.fact_social_protection
        """
    }

    for name, query in queries.items():

        result = connection.execute(
            text(query)
        )

        count = result.scalar()

        print(f"{name}: {count}")


# --------------------------------------------------
# Main
# --------------------------------------------------

def main():

    print("=" * 60)
    print("STAGING → DATA WAREHOUSE")
    print("=" * 60)

    engine = get_database_engine()

    with engine.begin() as connection:

        load_municipality_dimension(connection)

        load_category_dimension(connection)

        load_year_dimension(connection)

        load_fact_table(connection)

        verify_warehouse(connection)

    print("\nWarehouse load completed successfully.")


if __name__ == "__main__":
    main()