# Mechanic Shop API

Secure, production-oriented REST API for managing customers, mechanics, service tickets, and parts inventory. Built with **Flask** + **PostgreSQL**, secured by **JWT auth**, **rate limiting**, and **response caching**. API contracts are documented in **`static/swagger.yaml`** and a ready-to-import **Postman** collection sits at the repo root.

---

## Table of Contents
- [Overview](#overview)
- [Repository Layout](#repository-layout)
- [Quick Start](#quick-start)
- [Configuration](#configuration)
- [Authentication](#authentication)
- [Blueprints & Endpoints](#blueprints--endpoints)
- [Rate Limiting & Caching](#rate-limiting--caching)
- [Testing & CI](#testing--ci)
- [Deployment (Render)](#deployment-render)
- [Troubleshooting](#troubleshooting)
- [License](#license)

---

## Overview

This project demonstrates secure API design and operational hygiene:
- JWT token issuance and verification with role claims
- Route-level authorization decorators
- Rate limiting (Flask-Limiter) and response caching (Flask-Caching)
- Clean SQLAlchemy models with many-to-many relations
- Pagination on read-heavy endpoints
- Human-friendly documentation (Swagger + Postman)
- CI pipeline with GitHub Actions

---

## Repository Layout

```
MECHANIC_SHOP/
├── .github/
│   └── workflows/
│       └── main.yaml                    # CI (tests/build, optional deploy trigger)
├── app/
│   ├── blueprints/
│   │   ├── customers/
│   │   │   ├── __init__.py
│   │   │   ├── routes.py
│   │   │   └── schemas.py
│   │   ├── inventory/
│   │   │   ├── __init__.py
│   │   │   ├── routes.py
│   │   │   └── schemas.py
│   │   ├── mechanics/
│   │   │   ├── __init__.py
│   │   │   ├── routes.py
│   │   │   └── schemas.py
│   │   └── service_tickets/
│   │       ├── __init__.py
│   │       ├── routes.py
│   │       └── schemas.py
│   ├── static/
│   │   └── swagger.yaml                 # OpenAPI/Swagger spec
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── config.py                    # Config classes (Dev/Prod), env parsing
│   │   ├── extensions.py                # db, migrate, cache, limiter, etc.
│   │   └── util.py                      # encode_token(), token_required, helpers
│   └── models.py                        # SQLAlchemy models & relationships
├── instance/                            # instance-level files (ignored in prod)
├── tests/                               # pytest suites
├── .env                                 # local env vars (DO NOT COMMIT real secrets)
├── flask_app.py                         # create_app() factory & WSGI entrypoint
├── mechanic_shop.postman_collection.json
├── requirements.txt
└── venv/                                # optional local virtualenv (not used by CI)
```

> Folder names and files above mirror the repository screenshots.

---

## Quick Start

### 1) Prerequisites
- Python 3.11+, PostgreSQL 14+
- Create a database and a user with least-privileged access

### 2) Install & run (development)
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Environment (export or use .env)
export FLASK_APP=flask_app:create_app
export FLASK_ENV=development
export DATABASE_URL=postgresql://user:pass@localhost:5432/mechanic_api
export SECRET_KEY='long-random-string'

flask run
# or: gunicorn -w 4 'flask_app:create_app()'
```

### 3) Database migrations (if enabled)
```bash
# If Flask-Migrate/Alembic is wired in utils/extensions.py
flask db upgrade
```

### 4) Try it
- Import **`mechanic_shop.postman_collection.json`** into Postman
- Set `{{baseUrl}}` to your API (e.g., `http://127.0.0.1:5000`)
- Call `/login`, copy the token into `{{token}}`, then hit protected routes

---

## Configuration

Core settings are read from environment variables (see `app/utils/config.py`). Common values:

| Variable | Purpose | Example |
|---|---|---|
| `SECRET_KEY` | JWT signing key | `super-long-random` |
| `DATABASE_URL` | Postgres URI | `postgresql://user:pass@host:5432/db` |
| `FLASK_ENV` | `development` or `production` | `production` |
| `JWT_ALG` | Signing algorithm (`HS256`/`RS256`) | `HS256` (local) |
| `TOKEN_TTL_MIN` | Access token lifetime | `30` |
| `GLOBAL_RATE_LIMIT` | Optional default limit | `100/minute` |
| `CACHE_TYPE`/`CACHE_REDIS_URL` | Flask-Caching backend | `redis://...` |

Development uses `.env` (via python-dotenv). Production uses platform secrets (Render).

---

## Authentication

- **Login**: `POST /login` with `email` and `password` returns a **JWT** tied to `customer_id`
- **Bearer**: `Authorization: Bearer <token>` on protected routes
- **Decorator**: `@token_required` (from `app/utils/util.py`) validates the token and injects the `customer_id`
- Optional: mechanic role token encoder + `@mechanic_required` guard

**Example**  
```bash
curl -s -X POST "$BASE/login"   -H "Content-Type: application/json"   -d '{"email":"customer@example.com","password":"password123"}'
# → { "token": "..." }
```

---

## Blueprints & Endpoints

Blueprints live under `app/blueprints/` and are registered in `flask_app.py` with url_prefixes similar to the following. Adjust the prefixes below if you changed them in `__init__.py`.

### Customers (`/customers`)
- `GET /customers` — list customers (with **pagination**)

### Mechanics (`/mechanics`)
- `GET /mechanics/leaderboard` — ordered by tickets worked

### Service Tickets (`/service_tickets`)
- `PUT /service_tickets/<id>/edit` — add/remove mechanics using `add_ids`/`remove_ids`
- `GET /my-tickets` — returns tickets for the authenticated customer (Bearer token)

### Inventory (`/inventory`)
- `GET /inventory` — list parts
- `POST /inventory` — create part (Bearer)
- `GET /inventory/<id>` — get part
- `PUT /inventory/<id>` — update part (Bearer)
- `DELETE /inventory/<id>` — delete part (Bearer)

**Swagger/OpenAPI** lives at `app/static/swagger.yaml`. Serve it via your preferred Swagger UI or open it directly in an IDE renderer.

---

## Rate Limiting & Caching

- Configure **per-route** limits in blueprints using **Flask-Limiter**.  
- Optionally set a **default** `GLOBAL_RATE_LIMIT` (e.g., `100/minute`) to blanket all routes.  
- Use **Flask-Caching** for read-heavy endpoints (leaderboard, inventory list) and **invalidate on writes**.

---

## Testing & CI

- Tests live in `tests/` and run with `pytest -q`.
- CI pipeline is defined in `.github/workflows/main.yaml` (build + tests; optional deploy trigger).

```bash
pytest -q
```

> Keep secrets out of VCS; use `.env.sample` locally and repo secrets in CI.

---

## Deployment (Render)

1. Create a **Web Service** on Render pointing at this repo.  
2. Add env vars: `FLASK_ENV=production`, `SECRET_KEY`, `DATABASE_URL`.  
3. Start command: `gunicorn -w 4 'flask_app:create_app()'`.  
4. Update `static/swagger.yaml` server URL to your live base URL and ensure **HTTPS** is enforced.  
5. If you wired the GitHub Actions deploy step, ensure `RENDER_API_KEY` and `RENDER_SERVICE_ID` are set as repo secrets.

---

## Troubleshooting

- **401 Unauthorized**: invalid/missing Bearer token; log in again and retry.  
- **429 Too Many Requests**: rate limit hit; lower frequency or adjust limits.  
- **DB connection**: verify `DATABASE_URL`, user permissions, and network route.  
- **CORS**: add allowed origins/headers for your frontend.  
- **Swagger not loading**: check the path to `app/static/swagger.yaml` and any static-file config.

---

## License
