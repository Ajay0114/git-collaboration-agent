# Git Collaboration Intelligence Agent

M1 provides the application foundation: a FastAPI service, asynchronous PostgreSQL connectivity, Redis connectivity, database migrations, and local development infrastructure. GitHub monitoring, conflict detection, AI, MCP, and external collaboration integrations are not part of this milestone.

## Architecture

- `app/api/routes`: HTTP endpoints, including liveness and dependency readiness.
- `app/core`: centralized environment-based settings and structured logging.
- `app/db`: SQLAlchemy 2.x async engine/session and declarative base.
- `app/worker`: Celery application configuration using Redis as its broker.
- `alembic`: database migration environment.
- `tests`: automated API and readiness-check tests.
- Docker Compose runs PostgreSQL and Redis with health checks; the API runs locally in the Python virtual environment.

## Local setup

Requirements: Python 3.12, Docker with the Compose plugin, and a running Docker daemon.

Copy the example environment file using the command for your platform:

```bash
# Linux/macOS
cp .env.example .env
```

```powershell
# Windows PowerShell
Copy-Item .env.example .env
```

Edit `.env` and set a local `POSTGRES_PASSWORD`. Keep `.env` private; it is ignored by Git. Ensure the password in `DATABASE_URL` matches `POSTGRES_PASSWORD` (URL-encode special characters used in the URL).

Create and activate the Python 3.12 virtual environment, then install the project and development dependencies from `pyproject.toml`:

```bash
# Linux/macOS
python3 -m venv .venv
source .venv/bin/activate
```

```powershell
# Windows PowerShell
py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation due to its execution policy, activate the environment for the current session with `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process`, then run `.venv\Scripts\Activate.ps1` again.

With `.venv` active on either platform, install the dependencies (including the `dev` extra, which provides Pytest, HTTPX, pytest-asyncio, and Ruff):

```bash
python -m pip install --upgrade pip
python -m pip install -e '.[dev]'
```

Start PostgreSQL and Redis after confirming Docker is available:

```bash
docker info
docker compose up -d --wait
```

Apply migrations and run the API:

```bash
alembic upgrade head
uvicorn app.main:app --reload
```

The API listens at `http://127.0.0.1:8000` by default. `GET /health` is a liveness check. `GET /ready` checks PostgreSQL and Redis independently and returns HTTP 503 with per-component details if either check fails.

## Tests and useful commands

Run tests with the project environment active (or invoke its executable directly):

```bash
.venv/bin/python -m pytest
```

```powershell
.venv\Scripts\python.exe -m pytest
```

Other commands:

```bash
docker compose ps
docker compose logs -f postgres redis
docker compose down             # Preserve PostgreSQL data
# docker compose down -v        # Destructively remove PostgreSQL data
```

PostgreSQL data is stored in the named `postgres_data` Docker volume. Compose health checks are available for both services. Do not use the example password outside local development.
