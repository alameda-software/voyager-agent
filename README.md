# VoyagerAgent (VA)

> Travel agent in your pocket — chat-based app powered by AI.

## Tech Stack

| Layer | Technology |
|---|---|
| **Frontend** | Expo (React Native) |
| **Backend** | Python + FastAPI |
| **Agent** | LangChain |
| **Database** | PostgreSQL + Redis |
| **APIs** | Amadeus (flights, hotels, cars) |
| **Dev** | Docker Compose / Dokploy |
| **Prod** | AWS |

## Quick Start

### 1. Backend + Infra (Docker)

```bash
# Copy env template
cp services/api/.env.example services/api/.env

# Edit with your API keys
# OPENAI_API_KEY, AMADEUS_API_KEY, AMADEUS_API_SECRET

# Start everything
make up

# Run migrations
make migrate

# API docs → http://localhost:8000/docs
```

### 2. Mobile App (on your Mac)

```bash
cd apps/mobile
npm install
npx expo start
```

Scan QR with Expo Go (Android) or camera (iOS simulator).

## Project Structure

```
voyager-agent/
├── apps/
│   └── mobile/              # Expo React Native app
├── services/
│   └── api/                 # FastAPI backend
├── packages/
│   └── shared/              # Shared types/config
├── docker/                  # Docker Compose configs
├── docs/                    # Documentation
└── Makefile
```

## Commands

| Command | Description |
|---|---|
| `make up` | Start backend, Postgres, Redis |
| `make down` | Stop containers |
| `make migrate` | Run DB migrations |
| `make logs` | Tail API logs |
| `make reset` | Full reset (data + caches) |

## License

Private — Alameda Software
