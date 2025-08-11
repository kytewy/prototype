# FastAPI + Next.js Starter Template with Docker

This is a minimal starter template combining a FastAPI backend and a Next.js frontend, containerized with Docker and Docker Compose. It includes sample tests for both backend (pytest) and frontend (Vitest).

Use this project as a base to quickly prototype full-stack apps with modern Python and React/Next.js — extend and customize as you go!

---

## Features

- FastAPI backend with sample endpoint and pytest test
- Next.js frontend with a simple page and Playwright test
- Dockerfiles for backend and frontend
- Docker Compose to run both services together
- Makefile with commands to build, run, test, and clean environment

---

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) installed
- [Make](https://www.gnu.org/software/make/) installed (or run commands manually)

---

## Quickstart

### 1. Build and run backend + frontend (detached)

```bash
make dev
```

```bash
docker-compose up --build -d
```

### 2. Run backend tests

```bash
make test-back
```

Runs pytest inside the backend container.

### 3. Run frontend tests

Runs Vitest tests inside the frontend container.

```bash
make test-front
```

### 4. Clean up containers and volumes

Stops and removes containers, networks, volumes, and orphans.

```bash
make clean
```

### Extending this project

- Add more backend routes: Modify FastAPI code in backend/app/main.py.
- Add backend tests: Create more pytest test files under backend/tests/.
- Add frontend pages: Extend Next.js pages inside frontend/pages/.
- Add frontend tests: Add Vitest test files inside frontend/tests/.
- Add environment variables: Use Docker Compose environment variables for config.
- Add databases or other services: Extend docker-compose.yml with databases like PostgreSQL, Redis, etc.

### Notes

- Frontend Docker uses node:20-bookworm image for Next.js and Vitest compatibility.
- Backend uses Python 3.11 slim image.
- Frontend uses pnpm for package management.
- The .next directory permissions are set to 777 to avoid permission issues with Docker volumes.
- Use `make debug-back` or `make debug-front` to clean, rebuild, and test backend or frontend respectively.
- Use `make nuke` to completely rebuild the frontend container from scratch and run tests.
