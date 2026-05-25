from pathlib import Path

from alembic import command
from alembic.config import Config


def run_migrations() -> None:
    """Apply pending Alembic revisions using the same DATABASE_URL as the app."""
    project_root = Path(__file__).resolve().parents[2]
    alembic_cfg = Config(str(project_root / "alembic.ini"))
    alembic_cfg.set_main_option("script_location", str(project_root / "alembic"))
    command.upgrade(alembic_cfg, "head")
