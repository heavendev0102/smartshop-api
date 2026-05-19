"""Fix alembic_version when it points to a deleted revision."""
from sqlalchemy import create_engine, text

from app.core.config import settings

engine = create_engine(settings.database_url_sync)

with engine.connect() as conn:
    rows = conn.execute(text("SELECT version_num FROM alembic_version")).fetchall()
    print("Before:", rows)

    conn.execute(
        text("UPDATE alembic_version SET version_num = 'a9a5cb6504e2'")
    )
    conn.commit()

    rows = conn.execute(text("SELECT version_num FROM alembic_version")).fetchall()
    print("After:", rows)

print("Done. Run: alembic upgrade head")
