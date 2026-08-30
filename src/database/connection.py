import os

from dotenv import load_dotenv
from sqlalchemy import create_engine


load_dotenv()


def get_database_engine():
    """Create SQLAlchemy engine for PostgreSQL."""

    host = os.getenv("POSTGRES_HOST")
    port = os.getenv("POSTGRES_PORT")
    database = os.getenv("POSTGRES_DB")
    user = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")

    if not all([host, port, database, user, password]):
        raise ValueError(
            "Database environment variables are not configured."
        )

    connection_url = (
        f"postgresql+psycopg://"
        f"{user}:{password}@{host}:{port}/{database}"
    )

    return create_engine(connection_url)