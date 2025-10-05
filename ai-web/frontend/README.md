# Frontend

This Vite-powered React app mirrors the feature-oriented structure taught in the
AI in Web Programming labs. Each feature owns a `hooks/` folder for data-fetching
logic and a `components/` folder for presentational UI.

## Development

```bash
npm install
npm run dev
```

The app expects `VITE_API_BASE` to point at the FastAPI backend. When using the
provided `docker-compose.yml`, the variable is forwarded automatically. For a
standalone dev server, copy `.env.example` to `.env` and update the host/port as
needed.

## Adding a new feature

1. Follow the backend workflow in [`../docs/feature-workflow.md`](../docs/feature-workflow.md)
   to create a service and router.
2. Create a new folder under [`src/features`](src/features) with `hooks/` and
   `components/` subdirectories. Export a hook that wraps API calls via
   [`src/lib/api.js`](src/lib/api.js) and a component that documents its props with
   `prop-types`.
3. Compose the new feature inside [`src/App.jsx`](src/App.jsx) so the UI surfaces
   both the teaching copy and the interactive demo.

For AI-powered flows, keep secrets on the backend by default. The optional
`VITE_GEMINI_API_KEY` entry in `.env.example` is available only if a lesson
requires direct browser access to Gemini.
