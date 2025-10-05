# AI in Web Programming Lab Notebooks

A collection of weekly lab notebooks lives under `ai-web/labs`. Each notebook
follows the same structure (objectives, learning outcomes, prerequisites, guided
steps, validation checks with local curl commands, and homework extensions)
while covering the specific topics from the course brief.

## Backend stack

The backend located at `ai-web/backend` is a FastAPI application served by
Uvicorn. A small `EchoIn` Pydantic model validates the JSON payload sent from the
frontend, while the `/health` route powers automated curl checks inside each
lab. During development the app loads environment variables via `python-dotenv`
so keys like `GEMINI_API_KEY` can be provided without committing secrets, and
`CORSMiddleware` whitelists the Vite dev server origin for local testing.

## Frontend stack

The React frontend in `ai-web/frontend` is scaffolded with Vite. Components such
as `App.jsx` demonstrate hook-based state management, and a reusable helper in
`src/lib/api.js` wraps `fetch` calls to the backend. Vite injects `VITE_API_BASE`
so the client knows where to send requests when running in Docker or against a
deployed API.

## Container orchestration

`docker-compose.yml` builds and runs the frontend and backend containers side by
side, publishing ports `5173` and `8000` to the host. The compose file mounts
source code for hot reload, forwards `VITE_API_BASE` to the frontend, and bind
mounts [`backend/.env`](ai-web/backend/.env) into the FastAPI container so
secrets like `GEMINI_API_KEY` are loaded consistently. Copy
[`backend/.env.example`](ai-web/backend/.env.example) when setting up a new
environment and restart the backend container after editing `.env`.

## Instructor workflow

See [`ai-web/docs/feature-workflow.md`](ai-web/docs/feature-workflow.md) for a
step-by-step walkthrough that shows how to add new routers/services on the
backend and matching hooks/components on the frontend. The document mirrors the
lab exercises and serves as a ready-to-teach script when extending the project
with AI-driven demos.

## Notebook generator

The script `generate_ai_web_lab_notebooks.py` programmatically scaffolds each
lab notebook. It ensures sections such as objectives, prerequisites, validation
steps, and homework prompts follow a consistent template across the course,
making it easier to maintain and extend the curriculum.
