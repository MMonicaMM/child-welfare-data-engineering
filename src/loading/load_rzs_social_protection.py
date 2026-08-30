from pathlib import Path
import sys

from sqlalchemy import text


PROJECT_ROOT = Path(__file__).resolve().parents[2]

sys.path.append(str(PROJECT_ROOT))


from src.database.connection import get_database_engine
from src.transformation.transform_rzs_social_protection import transform


TARGET_TABLE = "staging.rzs_social_protection"


def load_to_postgres(df):

    engine = get_database_engine()

    print("Loading data into PostgreSQL...")

    with engine.begin() as connection:

        for _, row in df.iterrows():

            query = text(
                """
                INSERT INTO staging.rzs_social_protection (
                    municipality,
                    municipality_code,
                    year,
                    category,
                    value,
                    source_id,
                    loaded_at
                )
                VALUES (
                    :municipality,
                    :municipality_code,
                    :year,
                    :category,
                    :value,
                    :source_id,
                    :loaded_at
                )
                ON CONFLICT (
                    source_id,
                    municipality_code,
                    year,
                    category
                )
                DO UPDATE SET
                    municipality = EXCLUDED.municipality,
                    value = EXCLUDED.value,
                    loaded_at = EXCLUDED.loaded_at;
                """
            )

            connection.execute(
                query,
                {
                    "municipality": row["municipality"],
                    "municipality_code": row["municipality_code"],
                    "year": row["year"],
                    "category": row["category"],
                    "value": row["value"],
                    "source_id": row["source_id"],
                    "loaded_at": row["loaded_at"],
                },
            )

    print(
        f"Processed {len(df)} rows."
    )


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

    print(
        f"Rows currently in {TARGET_TABLE}: {count}"
    )


def main():

    print("=" * 60)
    print("RZS SOCIAL PROTECTION LOAD")
    print("=" * 60)

    df = transform()

    print(
        f"\nTransformed rows: {len(df)}"
    )

    load_to_postgres(df)

    verify_load()

    print("\nLoad completed successfully.")


if __name__ == "__main__":
    main()