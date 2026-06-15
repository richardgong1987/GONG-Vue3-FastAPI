# Docker Compose Deployment

Five services run as independent containers, brought up with one command. Stateful
services (database + redis) persist their data in named volumes, so you can rebuild
the app without losing data and **without restarting the database every time**.

## Services

| Service          | Container         | Role                          | Host port |
|------------------|-------------------|-------------------------------|-----------|
| `ruoyi-frontend` | `ruoyi-frontend`  | Vue build served by nginx     | 12580     |
| `ruoyi-backend`  | `ruoyi-backend-*` | FastAPI app                   | 19099     |
| database         | `ruoyi-pg` / `ruoyi-mysql` | PostgreSQL 14 / MySQL 8 | 15432 / 13306 |
| `ruoyi-redis`    | `ruoyi-redis`     | Redis cache (AOF persistence) | 16379     |

nginx is the frontend container: it serves the static build and reverse-proxies
`/docker-api/` to the backend (`bin/nginx.docker*.conf`).

## Start everything (one command)

```bash
docker compose -f docker-compose.pg.yml up -d --build
```

Open the app at http://localhost:12580.

## Persistence

Database and redis data live in named volumes (`ruoyi-pg-data` /
`ruoyi-mysql-data`, `ruoyi-redis-data`). They survive `down` and rebuilds.

- The init SQL under `/docker-entrypoint-initdb.d/` runs **only on the first
  start** (when the data volume is empty). It is not re-applied on later starts.
- `docker compose down` stops and removes containers but **keeps** the volumes.
- `docker compose down -v` also deletes the volumes — this wipes the database.

## Rebuild the app without touching the database / cache

Because the database and redis are separate, long-lived containers, rebuild only
the app services. Postgres/MySQL and redis keep running with their data intact:

```bash
docker compose -f docker-compose.pg.yml up -d --build ruoyi-backend-pg ruoyi-frontend
```

## Notes

- `restart: unless-stopped` makes every container come back after a host reboot or
  crash, so the stack stays up without manual intervention.
- To switch DB credentials/ports, edit the relevant `.env.docker*` file in
  `ruoyi-fastapi-backend/` and the matching values in the compose file.
