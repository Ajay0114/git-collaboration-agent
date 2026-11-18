Step - 1 

    We are starting development of Git Collaboration Intelligence Agent.

    First, inspect the current working directory, Git repository status, available Python version, Docker version and installed dependencies.

    Our GitHub repository is:
    AjaykumarKothapally/git-collaboration-agent

    The project will monitor the maitaiane GitHub repository and detect potential merge conflicts between developers.

    For now, implement only M1: Project Foundation.

    Technology stack:
    - Python 3.12
    - FastAPI
    - PostgreSQL
    - SQLAlchemy 2.x
    - Alembic
    - Redis
    - Celery
    - Docker Compose
    - Pytest

    Requirements:
    1. Propose a modular project structure.
    2. Create the FastAPI application.
    3. Configure PostgreSQL and Redis using Docker Compose.
    4. Configure SQLAlchemy database connectivity.
    5. Configure Alembic.
    6. Implement GET /health and GET /ready.
    7. Implement environment-based configuration.
    8. Create .env.example and .gitignore.
    9. Add structured logging.
    10. Write initial automated tests.
    11. Document local setup and execution commands in README.md.

    Important rules:
    - Inspect before creating files.
    - Do not implement GitHub integration yet.
    - Do not implement AI or MCP yet.
    - Do not hardcode credentials.
    - Do not commit or push changes.
    - Explain the architecture before implementation.
    - Run tests and verify all implemented functionality.
    - Work incrementally and report any failures honestly.

    Start with environment inspection and the proposed implementation plan. Wait for my approval before creating files.


Step - 2
    Your proposed M1 architecture is approved.

    Proceed with implementation.

    Before creating files, incorporate these additional requirements:

    1. Create and use a Python virtual environment (.venv). Do not install application dependencies globally.
    2. Use pyproject.toml for dependency management and project configuration.
    3. Implement independent PostgreSQL and Redis connectivity checks in GET /ready.
    4. Return HTTP 503 when either dependency is unavailable, with meaningful component-level status details.
    5. Verify Docker daemon availability before attempting container startup.
    6. Keep secrets and .env files out of Git.
    7. Ensure Docker Compose services have persistent PostgreSQL storage and appropriate health checks.
    8. Use asynchronous FastAPI database connectivity where appropriate, without introducing unnecessary complexity.
    9. Keep application configuration centralized.
    10. Ensure all tests run using the project's virtual environment.

    Implementation rules:

    - Create files incrementally.
    - Explain important architectural decisions.
    - Run tests after implementation.
    - Fix errors before declaring M1 complete.
    - Do not commit or push anything.
    - Do not implement GitHub, MCP, Teams or AI integrations in M1.

    Proceed with M1 implementation now.