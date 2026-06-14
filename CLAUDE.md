# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

RuoYi-Vue3-FastAPI is a full-stack admin/RBAC rapid-development platform (若依). It is a monorepo with four independent sub-projects:

- `ruoyi-fastapi-backend/` — FastAPI + SQLAlchemy (async) + MySQL/PostgreSQL + Redis backend. This is where almost all server work happens.
- `ruoyi-fastapi-frontend/` — Vue 3 + Element Plus admin web UI (Vite).
- `ruoyi-fastapi-app/` — uni-app + Vue 3 mobile client (H5 / WeChat mini-program), managed with pnpm.
- `ruoyi-fastapi-test/` — Playwright + pytest end-to-end tests that drive the running frontend/backend.

Code, comments, and docstrings are predominantly in Chinese; match that convention when editing existing files.

## Commands

### Backend (`ruoyi-fastapi-backend/`)
```bash
pip3 install -r requirements.txt          # MySQL deps
pip3 install -r requirements-pg.txt       # PostgreSQL deps (alternative)
ruoyi app run --env=dev                   # run the server (preferred entrypoint, exposes a CLI)
python3 app.py                            # alternative direct uvicorn entrypoint
ruff check .                              # lint (CI gate: "Ruff Check" workflow)
ruff format .                             # format
```
The `ruoyi` command comes from `pyproject.toml` (`project.scripts: ruoyi = "cli.main:main"`); install the backend package (`pip install -e .`) to get it on PATH. Run `ruoyi --help` to discover sub-commands (`app`, `db`, `cache`, `config`, `crypto`, `gen`, `job`, `ops`, `dev`). See `docs/cli_usage.md`.

Environment is selected by `--env` and loaded from `.env.<env>` files (`.env.dev`, `.env.prod`, `.env.dockermy`, `.env.dockerpg`) at the backend root. Configure DB/Redis there before first run, then load the SQL schema from `sql/ruoyi-fastapi.sql` (MySQL) or `sql/ruoyi-fastapi-pg.sql` (PostgreSQL).

### Frontend (`ruoyi-fastapi-frontend/`)
```bash
npm install --registry=https://registry.npmmirror.com
npm run dev            # dev server (default port 80)
npm run build:prod     # production build
npm run build:stage    # staging build
```

### Mobile (`ruoyi-fastapi-app/`)
```bash
pnpm install
pnpm dev:h5            # H5
pnpm dev:mp-weixin     # WeChat mini-program
```

### E2E tests (`ruoyi-fastapi-test/`)
```bash
pip3 install -r requirements.txt
playwright install
pytest                                   # run all
pytest test_login.py                     # single file
pytest test_login.py::test_login_page_loads   # single test
```
Tests require the frontend and backend to be running; `common/config.py` holds the target URLs.

### Docker
```bash
docker compose -f docker-compose.my.yml up -d --build   # MySQL stack
docker compose -f docker-compose.pg.yml up -d --build   # PostgreSQL stack
```

## Backend Architecture

### Layered, feature-module structure
The backend is organized into `module_*` packages, each a bounded feature area: `module_admin` (core RBAC/system mgmt), `module_ai` (AI model mgmt + chat), `module_generator` (code generation from DB tables), `module_task` (scheduled jobs). Every module follows the same four-layer split:

```
module_x/
  controller/   # FastAPI routes (APIRouterPro), request/response handling only
  service/      # business logic, orchestration, transaction scope
  dao/          # SQLAlchemy queries (data access only)
  entity/
    vo/         # Pydantic models — request/response/command/query (the wire & service shapes)
    do/         # SQLAlchemy ORM models (DeclarativeBase, DB tables, e.g. SysUser)
```
Dependency direction is controller → service → dao → entity. `vo` (value objects / Pydantic) cross all layers; `do` (ORM) stays in dao/service. Keep business rules in `service`, not in controllers or dao.

### Auto-registered routers
There is **no central router include list**. `common/router.RouterRegister` globs `*/controller/[!_]*.py`, imports each module, and registers every module-level `APIRouterPro` instance it finds (see `auto_register_routers` called from `server.py`). Routers are ordered by their `order_num` (lower = earlier). To add an endpoint group, create a `*_controller.py` defining a module-level `APIRouterPro(prefix=..., order_num=..., tags=..., dependencies=[...])` — it is wired up automatically.

### Cross-cutting concerns (read these before adding endpoints)
- `common/aspect/` — dependency-injection helpers attached to routes: `pre_auth.PreAuthDependency` / `CurrentUserDependency` (auth + current user), `db_seesion.DBSessionDependency` (async session), `data_scope.DataScopeDependency` (row-level data scope filtering by dept/role), `interface_auth.UserInterfaceAuthDependency` (permission-string checks). Controllers compose these as FastAPI `Depends`.
- `common/annotation/` — decorators applied to controller functions: `@Log` (operation logging), `@ApiCache` / `@ApiCacheEvict` (Redis caching), `@ApiRateLimit` (rate limiting). Auth/validation use `pydantic_validation_decorator.ValidateFields`.
- `common/vo.py` — shared response envelopes (`ResponseBaseModel`, `DataResponseModel`, `PageResponseModel`, `PageModel`). Build responses via `utils/response_util.ResponseUtil`.
- `middlewares/` — registered in `middlewares/handle.py`: CORS, gzip, demo-mode guard, request context/trace, response headers, and **transport-layer crypto** (`transport_crypto_middleware.py`) which transparently decrypts requests / encrypts responses with rotating keys (see `docs/transport_crypto_config.md`).
- `exceptions/` — custom exceptions in `exception.py`, global handlers wired in `handle.py`.

### Infrastructure / lifespan
`server.py` `create_app()` builds the app with an async lifespan that: creates tables (`config/get_db.py`), initializes Redis (`config/get_redis.py`), starts the APScheduler-based job scheduler (`config/get_scheduler.py`), mounts sub-applications (`sub_applications/`, e.g. static files), and runs background tasks (distributed-lock renewal, a Redis-stream log aggregator via `LogAggregatorService`). `app.py` is the uvicorn entrypoint (`factory=True`).

### Config
All settings are Pydantic `BaseSettings` classes in `config/env.py` (`AppConfig`, `JwtConfig`, `DataBaseConfig`, `RedisConfig`, `UploadConfig`, …), populated from the active `.env.<env>` file. `db_type` switches between `mysql` and `postgresql`; SQL dialect handling uses `sqlglot`. Use these config objects rather than reading env vars directly.

### Database migrations
Alembic is configured under `alembic/` (env, README, `script.py.mako`). The baseline schema, however, ships as raw SQL in `sql/`.

## Conventions

- **Lint/format:** Ruff with single quotes, line-length 120, target py310, and a broad rule set (see `ruoyi-fastapi-test/ruff.toml` and backend `ruff.toml`). `max-args = 10`. Run `ruff check`/`ruff format` before committing backend changes — CI enforces it.
- **Async everywhere:** SQLAlchemy async sessions, `asyncmy`/`asyncpg` drivers, async controllers/services. Don't introduce blocking DB/IO in request paths.
- **Naming:** ORM models are `SysXxx` in `entity/do/*_do.py`; Pydantic models are `XxxModel` (e.g. `AddUserModel`, `UserPageQueryModel`) in `entity/vo/*_vo.py`. Controllers/services/daos are suffixed `_controller`/`_service`/`_dao`.
- **AI providers:** `module_ai` integrates many LLM SDKs (anthropic, openai, google-genai, litellm, agno, etc., pinned in `requirements.txt`). When touching LLM code, default to the latest Claude models.
- **Commits:** Conventional Chinese commit messages (`feat: …`, `fix: …`) with a trailing PR number, e.g. `feat: 新增cli系统 (#103)`.
