# Full-stack feature workflow

This guide documents the classroom-friendly workflow for adding a new feature to
the AI in Web Programming labs. Follow the steps sequentially so the backend and
frontend stay in sync and mirror the structure students build in Lab 01–03.

## 1. Design the service layer

1. Create a module under [`app/services`](../backend/app/services) that contains
   the core business logic. Use [`services/echo.py`](../backend/app/services/echo.py)
   and [`services/gemini.py`](../backend/app/services/gemini.py) as references for
   docstring-heavy helpers and error handling.
2. Load secrets through environment variables (`python-dotenv` is wired up in
   [`app/main.py`](../backend/app/main.py)). Provide clear error messages so
   instructors can demo misconfiguration scenarios.

## 2. Expose the functionality via a router

1. Add a new router module to [`app/routers`](../backend/app/routers). Keep the
   handlers thin by importing the service function you created in the previous
   step. See [`routers/echo.py`](../backend/app/routers/echo.py) and
   [`routers/gemini.py`](../backend/app/routers/gemini.py) for examples of
   defining request/response models next to the route.
2. Register the router inside [`app/main.py`](../backend/app/main.py) with
   `app.include_router`. This keeps the application entry point as the single
   place that assembles middleware and routes.

## 3. Add a matching frontend feature

1. Scaffold a new folder in [`frontend/src/features`](../frontend/src/features)
   with `components/` and `hooks/` subdirectories. Each feature exposes a hook
   that performs data fetching (e.g. [`useEchoForm`](../frontend/src/features/echo/hooks/useEchoForm.js)
   and [`useLessonOutlineForm`](../frontend/src/features/gemini/hooks/useLessonOutlineForm.js)).
2. Build a presentational component that receives the hook’s state/handlers via
   props. [`EchoForm`](../frontend/src/features/echo/components/EchoForm.jsx) and
   [`LessonOutlineForm`](../frontend/src/features/gemini/components/LessonOutlineForm.jsx)
   showcase how to document props with `prop-types` and render helpful teaching
   copy alongside the UI.
3. Update [`src/App.jsx`](../frontend/src/App.jsx) to import the new feature and
   render it in the layout. Keep the application shell focused on composition so
   students can scan it quickly during lectures.

## 4. Wire up environment variables

1. Document new keys in [`backend/.env.example`](../backend/.env.example) and
   [`frontend/.env.example`](../frontend/.env.example). Copy the backend template
   to [`backend/.env`](../backend/.env) and update the real values before
   launching Docker; the compose stack bind-mounts that file directly into the
   FastAPI container. Restart the backend service after editing `.env` so
   `python-dotenv` reloads the secrets.
2. When introducing AI-powered flows, store API keys on the backend and proxy
   requests through FastAPI. The Gemini example keeps secrets server-side while
   the frontend calls `/ai/lesson-outline` via [`lib/api.js`](../frontend/src/lib/api.js).

## 5. Validate the end-to-end flow

1. Start the backend with `uvicorn app.main:app --reload` and the frontend with
   `npm run dev` from `ai-web/frontend`. Confirm both sections of the UI load in
   the browser.
2. Use `curl` to test new endpoints directly. For example:

   ```bash
   curl -X POST http://localhost:8000/ai/lesson-outline \
     -H 'Content-Type: application/json' \
     -d '{"topic": "State management in React"}'
   ```

3. Demonstrate error handling by temporarily removing environment variables or
   by adjusting query parameters (e.g. hitting `/flaky-echo?failures=3`). Discuss
   how the frontend surfaces these failures to students.

Following this workflow keeps the curriculum consistent and gives learners a
repeatable process for building their own features.
