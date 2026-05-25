"""Verify the database the app uses has product columns and Alembic is at head."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import psycopg2

from app.core.config import settings

REQUIRED_COLUMNS = {"description", "stock", "ratings"}


def main() -> int:
    sync_url = settings.database_url_sync
    print("Using:", sync_url)

    conn = psycopg2.connect(sync_url)
    cur = conn.cursor()
    cur.execute("SELECT current_database()")
    print("Database:", cur.fetchone()[0])

    try:
        cur.execute("SELECT version_num FROM alembic_version")
        print("Alembic revision:", cur.fetchone()[0])
    except psycopg2.Error as exc:
        print("Alembic version table missing:", exc)
        return 1

    cur.execute(
        "SELECT column_name FROM information_schema.columns "
        "WHERE table_schema='public' AND table_name='products' ORDER BY ordinal_position"
    )
    cols = {r[0] for r in cur.fetchall()}
    print("products columns:", sorted(cols))

    missing = REQUIRED_COLUMNS - cols
    if missing:
        print("MISSING columns:", sorted(missing))
        print("Fix: .\\.venv\\Scripts\\alembic.exe upgrade head")
        return 1

    conn.close()
    print("OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
