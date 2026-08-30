from sqlalchemy import text

from connection import get_database_engine


engine = get_database_engine()

with engine.connect() as connection:
    result = connection.execute(
        text("SELECT current_database(), current_user;")
    )

    print(result.fetchone())