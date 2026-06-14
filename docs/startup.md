# Startup Guide: Backend & Frontend

How to start the **backend (FastAPI)** and **frontend (Vue3 + Vite)** locally, how to check whether they are already running, and how to stop them.

> Ports (from `.env.dev` / frontend config):
> - Backend: `0.0.0.0:9099` (`APP_ROOT_PATH = /dev-api`)
> - Frontend: `http://localhost:80` (Vite dev server)
> - Database: PostgreSQL `127.0.0.1:5432`, database `ruoyi-fastapi`
> - Redis: `127.0.0.1:6379`

---

## 0. Prerequisites

Before starting the backend, make sure the dependent services are running:

```bash
# Check that PostgreSQL and Redis are listening
lsof -nP -iTCP:5432 -sTCP:LISTEN   # PostgreSQL
lsof -nP -iTCP:6379 -sTCP:LISTEN   # Redis
```

On first run, import the database schema:

```bash
# PostgreSQL (current .env.dev uses postgresql)
psql -h 127.0.0.1 -U <user> -d ruoyi-fastapi -f ruoyi-fastapi-backend/sql/ruoyi-fastapi-pg.sql

# If using MySQL instead: sql/ruoyi-fastapi.sql
```

---

## 1. Start the Backend (`ruoyi-fastapi-backend/`)

### 1.1 Install dependencies (first run or when dependencies change)

```bash
cd ruoyi-fastapi-backend
pip3 install -r requirements-pg.txt   # current setup uses PostgreSQL
# If using MySQL: pip3 install -r requirements.txt
```

### 1.2 Start (choose one)

**Option A — CLI (recommended)**

```bash
cd ruoyi-fastapi-backend
pip install -e .          # first time only, puts the `ruoyi` command on PATH
ruoyi app run --env=dev
```

**Option B — run the entry script directly**

```bash
cd ruoyi-fastapi-backend
python3 app.py --env dev
```

Both read `.env.dev` and start uvicorn on `APP_HOST:APP_PORT` (`0.0.0.0:9099`). With `APP_RELOAD=true`, hot reload is enabled.

The environment is selected with `--env`, mapping to a `.env.<env>` file at the backend root: `dev` / `prod` / `dockermy` / `dockerpg`.

### 1.3 Verify the backend

```bash
curl http://127.0.0.1:9099/dev-api/docs    # Swagger docs
```

---

## 2. Start the Frontend (`ruoyi-fastapi-frontend/`)

### 2.1 Install dependencies (first run or when dependencies change)

```bash
cd ruoyi-fastapi-frontend
npm install --registry=https://registry.npmmirror.com
```

### 2.2 Start the dev server

```bash
cd ruoyi-fastapi-frontend
npm run dev               # equivalent to `vite`, listens on port 80 by default
```

> Note: port 80 is privileged on macOS/Linux. If startup fails, run with elevated privileges or change `server.port` in `vite.config.js`.

### 2.3 Verify the frontend

Open `http://localhost:80` in a browser. The frontend proxies `VITE_APP_BASE_API=/dev-api` to the backend on 9099.

Build outputs (not for development):

```bash
npm run build:prod        # production build
npm run build:stage       # staging build
```

---

## 3. Check Whether Services Are Already Running

Dev servers are long-lived processes: once started they keep running until manually stopped or the machine reboots. To check:

```bash
# By port
lsof -nP -iTCP:9099 -sTCP:LISTEN    # backend
lsof -nP -iTCP:80   -sTCP:LISTEN    # frontend

# By process name
ps aux | grep -E "app\.py|vite" | grep -v grep
```

If you see `python3 ... app.py --env dev` and `node ... /vite`, the services are already running in the background. This usually explains a "I didn't start it but it's still running" situation: a process from an earlier launch (terminal, IDE run config, or docker) was never stopped.

---

## 4. Stop Services

```bash
# Use the PIDs found above
kill <backend_PID>        # e.g. kill 40170
kill <frontend_PID>       # e.g. kill 39855

# Force kill if a process won't exit
kill -9 <PID>
```

One-liner to stop both by port:

```bash
kill $(lsof -nP -iTCP:9099 -iTCP:80 -sTCP:LISTEN -t | sort -u)
```

> With `APP_RELOAD=true`, the backend has a parent (reloader) and a child (worker). Killing the parent usually takes the child with it; if the child lingers, kill it separately.
> Do not kill the PostgreSQL, Redis, or editor `ruff server` processes — they are not part of the app itself.

---

## 5. Docker (Optional)

Bring up the whole stack (database + Redis + backend + frontend) without installing dependencies manually:

```bash
docker compose -f docker-compose.pg.yml up -d --build    # PostgreSQL stack
docker compose -f docker-compose.my.yml up -d --build    # MySQL stack
```
