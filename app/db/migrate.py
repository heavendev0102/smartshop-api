from pathlib import Path
import traceback

from alembic import command
from alembic.config import Config


def run_migrations() -> None:
    try:
        print("== Starting Alembic ==")

        project_root = Path(__file__).resolve().parents[2]

        alembic_cfg = Config(str(project_root / "alembic.ini"))
        alembic_cfg.set_main_option(
            "script_location",
            str(project_root / "alembic"),
        )

        command.upgrade(alembic_cfg, "head")

        print("== Alembic Finished ==")

    except Exception:
        print("========== ALEMBIC ERROR ==========")
        traceback.print_exc()
        raise