# VoyagerAgent

Pre-MVP AI concierge app with two test modes:

- `Voyager` for travel planning
- `Wedding` for wedding/vendor planning

The current stack is:

| Layer | Technology |
|---|---|
| Frontend | Expo / React Native |
| Backend | FastAPI |
| Database | PostgreSQL |
| Cache | Redis |
| Agent runtime | Shared concierge core + domain packs |

## Recommended Local Dev Flow

Use this setup for local development:

- PostgreSQL in Docker
- Redis in Docker
- FastAPI locally with `uvicorn`
- Expo locally for the frontend

This is the cleanest path for the current repo.

## Quick Commands

From the repo root:

```bash
make dev-db
make dev-api-setup
make migrate
make dev-api
```

In another terminal:

```bash
make dev-web
```

## 1. Start Database and Redis

From the repo root:

```bash
cd docker
docker compose up -d postgres redis
```

This exposes:

- Postgres at `localhost:15432`
- Redis at `localhost:6379`

To verify Postgres is up:

```bash
docker compose exec postgres psql -U postgres -l
```

## 2. Backend Setup

### Create backend env

```bash
cp services/api/.env.example services/api/.env
```

`services/api/.env` should look like:

```env
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:15432/voyager
REDIS_URL=redis://localhost:6379/0
JWT_SECRET=your-secret-key
JWT_ALGORITHM=HS256
OPENAI_API_KEY=
LLM_MODEL=gpt-4o-mini
```

### Create backend virtualenv

```bash
cd ../services/api
python3.11 -m venv .venv
source .venv/bin/activate
python -m ensurepip --upgrade
python -m pip install --upgrade pip setuptools wheel
python -m pip install -e ".[dev]"
```

### Run database migrations

```bash
./.venv/bin/alembic upgrade head
```

### Run the backend

```bash
./.venv/bin/uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend URLs:

- health: `http://localhost:8000/health`
- docs: `http://localhost:8000/docs`

The health endpoint should return:

```json
{"status":"healthy"}
```

## 3. Frontend Setup

### Create frontend env

```bash
cd ../../apps/mobile
cp .env.example .env
```

`apps/mobile/.env` should contain:

```env
EXPO_PUBLIC_API_URL=http://localhost:8000
```

### Install frontend dependencies

```bash
npm install
```

If npm gets stuck on old dependencies, reset the install:

```bash
rm -rf node_modules package-lock.json
npm install
```

### Run the frontend

For web:

```bash
npx expo start --web --clear
```

For mobile:

```bash
npx expo start
```

Do not use `npx start` or `npx start expo`. The correct command is `npx expo start`.

## Current App Flow

When the frontend opens, the first screen lets you choose:

- `Voyager`
- `Wedding`

Each button creates a backend conversation with a different `domain`, but both use the same shared concierge session engine.

## Useful Commands

| Command | Description |
|---|---|
| `make up` | Start API, Postgres, Redis in Docker |
| `make down` | Stop containers |
| `make restart` | Restart containers |
| `make logs` | Tail API logs |
| `make dev-db` | Start local Postgres and Redis only |
| `make dev-api-setup` | Create backend `.venv` and install dependencies |
| `make dev-api` | Run FastAPI locally with `uvicorn` |
| `make dev-web` | Run Expo web with cache clear |
| `make dev-mobile` | Run Expo mobile dev server |
| `make migrate` | Run Alembic migrations |
| `make db-shell` | Open Postgres shell in Docker |
| `make export-web` | Build a static web export from the Expo app |
| `make shell` | Open API container shell |
| `make reset` | Remove containers and local caches |

## Notes

- Auth is still stubbed, so the current app uses a lightweight guest user flow for testing.
- The backend session API is real; the domain recommendation logic is still fake-data pre-MVP logic.
- If the frontend cannot connect, first confirm `http://localhost:8000/health` works.
- If the frontend shows Axios `Network Error`, the usual causes are:
  `EXPO_PUBLIC_API_URL` is wrong, the backend is not running, or DB migrations were not applied.

## Deploy

The current repo is easiest to deploy as two parts:

1. Backend services
   FastAPI, Postgres, and Redis.
2. Frontend web build
   Static files exported from Expo web.

### Backend deploy

For staging or a small first deployment, the simplest path is:

- deploy `services/api` as a Docker service
- deploy Postgres as a managed database or Docker service
- deploy Redis as a managed service or Docker service
- set backend env vars in the target environment

Minimum backend env vars:

```env
DATABASE_URL=postgresql+asyncpg://postgres:postgres@<db-host>:5432/voyager
REDIS_URL=redis://<redis-host>:6379/0
JWT_SECRET=change-this
JWT_ALGORITHM=HS256
OPENAI_API_KEY=...
LLM_MODEL=gpt-4o-mini
```

Run migrations on the deployed backend before serving traffic:

```bash
./.venv/bin/alembic upgrade head
```

### Frontend deploy

Build the Expo web app:

```bash
make export-web
```

That creates static web output from `apps/mobile`.

Deploy those generated files to any static host, for example:

- Vercel
- Netlify
- Cloudflare Pages
- an S3 + CDN setup

The frontend environment must point to the deployed backend:

```env
EXPO_PUBLIC_API_URL=https://your-api-domain.com
```

### Practical first deployment shape

- backend API on a VPS or Dokploy
- Postgres and Redis on the same server or managed services
- Expo web export on a static host

That is the lowest-friction deployment model for the current codebase.

## License

Private.
