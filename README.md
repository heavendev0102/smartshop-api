# smartshop-api
FastAPI-based backend for SmartShop with PostgreSQL, authentication, and scalable API architecture.

## Local setup (Windows / PowerShell)

From the project root:

```powershell
python -m venv .venv
.\.venv\Scripts\pip install -r requirements.txt
.\.venv\Scripts\alembic.exe upgrade head
.\.venv\Scripts\python.exe scripts\check_db.py
.\.venv\Scripts\Activate.ps1
python -m uvicorn app.main:app --reload
```

Migrations also run automatically on app startup. If you see `column products.description does not exist`, your `app/.env` `DATABASE_URL` may point at a DB that has not been migrated — run `alembic upgrade head` against that database (e.g. uncomment the Render URL, migrate, then switch back).

```powershell
.\.venv\Scripts\Activate.ps1
python -m uvicorn app.main:app --reload
```

If `uvicorn` is not recognized, always use `python -m uvicorn` (with the virtual environment activated), or:

```powershell
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

API docs: http://127.0.0.1:8000/docs
