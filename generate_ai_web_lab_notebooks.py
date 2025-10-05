import nbformat as nbf
from pathlib import Path
import textwrap

ROOT = Path("ai-web/labs")
ROOT.mkdir(parents=True, exist_ok=True)


def md(text: str):
    return nbf.v4.new_markdown_cell(textwrap.dedent(text).strip())


def code(text: str):
    return nbf.v4.new_code_cell(textwrap.dedent(text).strip())


def notebook(title: str, cells):
    nb = nbf.v4.new_notebook()
    nb.cells = [
        md(
            f"# {title}\n\n*This lab notebook provides guided steps. All commands are intended for local execution.*"
        )
    ]
    nb.cells.extend(cells)
    return nb


def write_notebook(name: str, title: str, cells):
    path = ROOT / f"{name}.ipynb"
    with path.open("w", encoding="utf-8") as handle:
        nbf.write(notebook(title, cells), handle)
    print(f"Written: {path}")


def acceptance(commands: str, expectations: str):
    return md(
        f"## Validation / acceptance checks\n```bash\n# locally\n{commands}\n```\n- {expectations}\n- React development mode shows the described UI state without console errors."
    )


def homework(items):
    bullet = "\n".join(f"- {item}" for item in items)
    return md(f"## Homework / extensions\n{bullet}")


labs = []

# ---------------------------------------------------------------------------
# Lab 01
lab1_cells = [
    md(
        """## Objectives
- A FastAPI backend is scaffolded with health and echo routes.
- A Vite React frontend is outlined with modern tooling defaults.
- A Git repository is initialized with environment templates.
"""
    ),
    md(
        """## What will be learned
- The structure of a basic FastAPI service is reviewed.
- Development-time CORS settings are configured.
- Vite-powered React scaffolding steps are rehearsed.
- Git initialization practices are reinforced.
"""
    ),
    md(
        """## Prerequisites & install
The container workflow depends on these locally installed tools:

```bash
docker --version
docker compose version
git --version
```

After cloning the repository, build and start the services with Docker Compose:

```bash
cd ai-web
docker compose build
docker compose up
# Backend → http://localhost:8000
# Frontend → http://localhost:5173

# Shut the stack down when finished exploring:
docker compose down
```
"""
    ),
    md(
        """## Step-by-step tasks
Each step configures local source files that the Docker stack will mount so secrets remain outside the built images.

### Step 1: Backend folder layout and Dockerfile
A backend folder is created with starter FastAPI files and a Dockerfile that installs dependencies inside the image.
"""
    ),
    code(
        """
from pathlib import Path
base = Path("ai-web/backend")
base.mkdir(parents=True, exist_ok=True)

# Ensure the application package exists so FastAPI can locate modules.
(base / "app").mkdir(parents=True, exist_ok=True)
(base / "app" / "__init__.py").write_text("\n")

# Provide a sample environment file that documents required secrets.
(base / ".env.example").write_text('# Environment variables (never commit real keys)\nGEMINI_API_KEY=\n')

# List Python dependencies that will be installed within the backend container.
(base / "requirements.txt").write_text('''fastapi
uvicorn[standard]
pydantic
python-dotenv
google-generativeai
faiss-cpu
numpy
''')

# Create the FastAPI entrypoint with health and echo routes.
(base / "app" / "main.py").write_text('''from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class EchoIn(BaseModel):
    msg: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/echo")
def echo(payload: EchoIn):
    return {"msg": payload.msg}
''')

# Define a Dockerfile that installs dependencies and starts uvicorn.
(base / "Dockerfile").write_text('''FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \\n    PYTHONUNBUFFERED=1

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
''')

print("Backend scaffold and Dockerfile were written under ai-web/backend.")
"""
    ),
    md(
        """### Step 2: Frontend placeholders and Dockerfile
Frontend placeholders are positioned so Vite React components (`src/App.jsx`, `src/main.jsx`) can be customized while the generated `vite.config.js` continues to manage dev server defaults. A lightweight Dockerfile installs Node.js dependencies for the Vite dev server.
"""
    ),
    code(
        """
from pathlib import Path
frontend = Path("ai-web/frontend")
src = frontend / "src"
frontend.mkdir(parents=True, exist_ok=True)
src.mkdir(parents=True, exist_ok=True)

# Create a lib directory for shared utilities between components.
(src / "lib").mkdir(parents=True, exist_ok=True)

# Bootstrap a simple API helper with descriptive error handling.
(src / "lib" / "api.js").write_text('''const BASE = import.meta.env.VITE_API_BASE || "http://localhost:8000";

export async function post(path, body) {
  const res = await fetch(`${BASE}${path}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body)
  });
  if (!res.ok) {
    throw new Error(`HTTP ${res.status}`);
  }
  return res.json();
}
''')

# Author a basic demo interface that interacts with the echo endpoint.
(src / "App.jsx").write_text('''import { useState } from 'react';
import { post } from './lib/api';

function App() {
  const [msg, setMsg] = useState('hello');
  const [response, setResponse] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  async function handleSend() {
    setLoading(true);
    setError('');
    try {
      const json = await post('/echo', { msg });
      setResponse(json.msg);
    } catch (err) {
      setError(String(err));
    } finally {
      setLoading(false);
    }
  }

  return (
    <main style={{ padding: 24 }}>
      <h1>Lab 1 — Echo demo</h1>
      <input value={msg} onChange={(event) => setMsg(event.target.value)} />
      <button onClick={handleSend} disabled={loading}>Send</button>
      {loading && <p>Loading…</p>}
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <pre>{response}</pre>
    </main>
  );
}

export default App;
''')

# Mount the App component using Vite's modern entry point.
(src / "main.jsx").write_text('''import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App.jsx';

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
);
''')

# Ensure Vite configuration and HTML entrypoint exist for the dev server.
(frontend / "vite.config.js").write_text('''import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    host: true,
    port: 5173,
  },
});
''')

(frontend / "index.html").write_text('''<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/vite.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Lab 1 Echo Demo</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
  </body>
</html>
''')

# Provide a package.json that mirrors the Vite React starter dependencies.
(frontend / "package.json").write_text('''{
  "name": "frontend",
  "version": "0.0.0",
  "private": true,
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview --host"
  },
  "dependencies": {
    "react": "^18.3.1",
    "react-dom": "^18.3.1"
  },
  "devDependencies": {
    "@vitejs/plugin-react": "^4.3.1",
    "vite": "^5.2.0"
  }
}
''')

# Provide a Dockerfile that installs dependencies and runs the Vite dev server.
(frontend / "Dockerfile").write_text('''FROM node:20-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

CMD ["npm", "run", "dev", "--", "--host"]
''')

print("Frontend placeholders and Dockerfile were written under ai-web/frontend.")
"""
    ),
    md(
        """### Step 3: Docker Compose orchestration
A top-level `docker-compose.yml` is created so the backend and frontend can be started together with a single command.
"""
    ),
    code(
        """
from pathlib import Path
compose = Path("ai-web/docker-compose.yml")
compose.parent.mkdir(parents=True, exist_ok=True)

# Define services that mount local source for rapid iteration while keeping dependencies inside the containers.
compose.write_text('''version: "3.9"

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - GEMINI_API_KEY=${GEMINI_API_KEY:-}
    volumes:
      - ./backend/app:/app/app
      - ./backend/.env.example:/app/.env:ro

  frontend:
    build: ./frontend
    ports:
      - "5173:5173"
    environment:
      - VITE_API_BASE=http://localhost:8000
    volumes:
      - ./frontend/src:/app/src
      - ./frontend/vite.config.js:/app/vite.config.js
      - ./frontend/index.html:/app/index.html
      - ./frontend/package.json:/app/package.json
''')

print("Docker Compose file was written under ai-web/docker-compose.yml.")
"""
    ),
    md(
        """### Step 4: Git initialization
Git is initialized locally so changes can be tracked.
"""
    ),
    md(
        """
```bash
cd ai-web
git init
git add .
git commit -m "Lab 1 scaffold"
```
"""
    ),

    acceptance(
        "docker compose up -d\ncurl http://localhost:8000/health\ncurl -X POST http://localhost:8000/echo -H 'Content-Type: application/json' -d '{\"msg\":\"hello\"}'\ndocker compose down",
        "HTTP 200 responses include status \"ok\" and the echoed payload while the stack runs in Docker.",
    ),
    homework([
        "A README entry is expanded to document backend and frontend start commands.",
        "A GitHub repository is connected for remote backups.",
    ]),
]

labs.append(("Lab01_FastAPI_Vite_and_Git", "Lab 01 · FastAPI, Vite, and Git", lab1_cells))

# ---------------------------------------------------------------------------
# Lab 02
lab2_cells = [
    md(
        """## Objectives
- A robust fetch helper with retry logic is introduced.
- A controlled React form is configured with loading and error feedback.
- Friendly error messages are surfaced in the UI.
"""
    ),
    md(
        """## What will be learned
- Retry helpers are structured for frontend HTTP calls.
- Controlled form patterns in React are rehearsed.
- Error boundaries in simple forms are practiced.
"""
    ),
    md(
        """## Prerequisites & install
The following commands are intended for local execution.

```bash
cd ai-web/frontend
npm install
```
"""
    ),
    md(
        """## Step-by-step tasks
### Step 1: Retry helper placement
A retry helper is positioned under src/lib.
"""
    ),
    code(
        """
from pathlib import Path
lib = Path("ai-web/frontend/src/lib")
lib.mkdir(parents=True, exist_ok=True)
(lib / "retry.js").write_text('''export async function withRetry(fn, attempts = 2, delayMs = 400) {
  let lastError;
  for (let attempt = 0; attempt <= attempts; attempt += 1) {
    try {
      return await fn();
    } catch (error) {
      lastError = error;
    }
    await new Promise((resolve) => setTimeout(resolve, delayMs));
  }
  throw lastError;
}
''')
print("Retry helper was written.")
"""
    ),
    md(
        """### Step 2: Form integration
App.jsx is updated so the retry helper wraps the echo request and error states remain friendly.
"""
    ),
    code(
        """
from pathlib import Path
app_js = Path("ai-web/frontend/src/App.jsx")
text = app_js.read_text()
if "withRetry" not in text:
    text = text.replace(
        "import { post } from './lib/api';",
        "import { post } from './lib/api';\nimport { withRetry } from './lib/retry';",
    )
if "withRetry" in text and "withRetry(() => post" not in text:
    text = text.replace(
        "const json = await post('/echo', { msg });",
        "const json = await withRetry(() => post('/echo', { msg }), 2, 500);",
    )
if "setError(String(err));" in text:
    text = text.replace(
        "setError(String(err));",
        "setError('A temporary issue was encountered. Please try again.');",
    )
app_js.write_text(text)
print("App.jsx was adjusted for retry and friendly errors.")
"""
    ),
    acceptance(
        "curl -X POST http://localhost:8000/echo -H 'Content-Type: application/json' -d '{\"msg\":\"retry\"}'",
        "The echoed payload is returned successfully after transient failures are simulated.",
    ),
    homework([
        "Additional retry backoff strategies are outlined for future reference.",
        "Form validation rules are drafted to prevent empty submissions.",
    ]),
]

labs.append(("Lab02_HTTP_Forms_and_Retry", "Lab 02 · HTTP Forms and Retry", lab2_cells))

# ---------------------------------------------------------------------------
# Lab 03
lab3_cells = [
    md(
        """## Objectives
- A Gemini proxy endpoint is created in FastAPI.
- React chat UI components are connected to the proxy.
- API keys remain confined to the backend.
"""
    ),
    md(
        """## What will be learned
- Backend proxy patterns for hosted LLMs are practiced.
- Basic chat state management in React is reviewed.
- Environment variable usage is reinforced.
"""
    ),
    md(
        """## Prerequisites & install
The following commands are intended for local execution.

```bash
cd ai-web/backend
. .venv/bin/activate
pip install google-generativeai
```
"""
    ),
    md(
        """## Step-by-step tasks
### Step 1: Gemini helper module
A backend helper is written so Gemini calls are centralized.
"""
    ),
    code(
        """
from pathlib import Path
module = Path("ai-web/backend/app/llm.py")
module.parent.mkdir(parents=True, exist_ok=True)
module.write_text('''import os
from typing import Dict, List, Any

from google import genai


def chat(messages: List[Dict[str, Any]]) -> str:
  api_key = os.environ.get('GEMINI_API_KEY', '')
  if not api_key:
    raise RuntimeError('A backend API key is required.')
  client = genai.Client(api_key=api_key)
  response = client.models.generate_content(
      model="gemini-1.5-flash",
      contents=messages,
  )
  return response.text
''')
print("Gemini helper was written.")
"""
    ),
    md(
        """### Step 2: FastAPI route update
The FastAPI app is expanded with /api/chat.
"""
    ),
    code(
        """
from pathlib import Path
main_path = Path("ai-web/backend/app/main.py")
text = main_path.read_text()
addition = '''
from typing import List
from pydantic import BaseModel
from .llm import chat as gemini_chat


class ChatTurn(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: List[ChatTurn]


@app.post("/api/chat")
def chat_endpoint(request: ChatRequest):
    transcript = [
        {"role": turn.role, "parts": [turn.content]} for turn in request.messages
    ]
    text = gemini_chat(transcript)
    return {"text": text}
'''
if "chat_endpoint" not in text:
    main_path.write_text(text.rstrip() + "\n" + addition)
    print("FastAPI route was appended.")
else:
    print("FastAPI route already present.")
"""
    ),
    md(
        """### Step 3: React chat surface
A lightweight chat component is appended to App.jsx so the proxy is exercised.
"""
    ),
    code(
        """
from pathlib import Path
app_js = Path("ai-web/frontend/src/App.jsx")
app_js.write_text('''import React, { useState } from 'react';
import { post } from './lib/api';
import { withRetry } from './lib/retry';

function App() {
  const [messages, setMessages] = useState([{ role: 'user', content: 'Hello Gemini' }]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  async function handleSend(event) {
    event.preventDefault();
    const updated = [...messages, { role: 'user', content: input }];
    setMessages(updated);
    setLoading(true);
    setError('');
    try {
      const result = await withRetry(
        () => post('/api/chat', { messages: updated }),
        1,
        800
      );
      setMessages([...updated, { role: 'model', content: result.text }]);
      setInput('');
    } catch (err) {
      setError('The proxy was unreachable. Please try again.');
    } finally {
      setLoading(false);
    }
  }

  return (
    <main style={{ padding: 24 }}>
      <h1>Lab 3 — Gemini proxy chat</h1>
      <section>
        {messages.map((msg, index) => (
          <p key={index}>
            <strong>{msg.role}:</strong> {msg.content}
          </p>
        ))}
      </section>
      <form onSubmit={handleSend}>
        <input
          value={input}
          onChange={(event) => setInput(event.target.value)}
          placeholder="Type a follow-up"
        />
        <button type="submit" disabled={loading || !input}>Send</button>
      </form>
      {loading && <p>Awaiting proxy response…</p>}
      {error && <p style={{ color: 'red' }}>{error}</p>}
    </main>
  );
}

export default App;
''')
print("Chat UI was seeded.")
"""
    ),
    acceptance(
        "curl -X POST http://localhost:8000/api/chat -H 'Content-Type: application/json' -d '{\"messages\":[{\"role\":\"user\",\"content\":\"Hello\"}]}'",
        "A JSON response with a text field is produced by the backend proxy.",
    ),
    homework([
        "Streaming responses are researched for future enhancements.",
        "Chat history persistence is sketched for the next lab.",
    ]),
]

labs.append(("Lab03_Gemini_Proxy_Chat", "Lab 03 · Gemini Proxy Chat", lab3_cells))

# ---------------------------------------------------------------------------
# Additional labs

labs.append((
    "Lab04_Structured_JSON_and_Validation",
    "Lab 04 · Structured JSON and Validation",
    [
        md(
            """## Objectives
- A planner endpoint is produced that returns structured JSON.
- Pydantic validation is applied to enforce schema guarantees.
- Automatic repair strategies are outlined for invalid JSON.
"""
        ),
        md(
            """## What will be learned
- Structured JSON responses are validated on the backend.
- Error handling flows for invalid planner output are reviewed.
- Lightweight repair attempts are documented for client consumption.
"""
        ),
        md(
            """## Prerequisites & install
The following commands are intended for local execution.

```bash
cd ai-web/backend
. .venv/bin/activate
pip install pydantic
```
"""
        ),
        md(
            """## Step-by-step tasks
### Step 1: Planner schema definition
A schema is defined so planner responses remain consistent.
"""
        ),
        code(
            """
from pathlib import Path
planner_path = Path("ai-web/backend/app/planner.py")
planner_path.write_text('''from pydantic import BaseModel, Field, ValidationError
from typing import List


class Plan(BaseModel):
    goal: str = Field(..., description="High level objective")
    steps: List[str] = Field(default_factory=list, description="Ordered plan steps")


def build_plan(goal: str) -> Plan:
    steps = [
        "It is ensured that the goal is clarified.",
        "Resources are gathered to support the plan.",
        "Progress is reviewed upon completion.",
    ]
    return Plan(goal=goal, steps=steps)


def repair_plan(data: dict) -> Plan:
    try:
        return Plan(**data)
    except ValidationError as exc:
        fixed = {"goal": data.get("goal", "A goal was recorded."), "steps": []}
        for idx, issue in enumerate(exc.errors()):
            fixed["steps"].append(f"Step {idx + 1} was replaced because {issue['msg']}")
        return Plan(**fixed)
''')
print("Planner module was written.")
"""
        ),
        md(
            """### Step 2: API exposure
The planner endpoint is exposed at /api/plan with validation.
"""
        ),
        code(
            """
from pathlib import Path
main_path = Path("ai-web/backend/app/main.py")
text = main_path.read_text()
if "plan_endpoint" not in text:
    addition = '''
from pydantic import BaseModel
from .planner import build_plan, repair_plan


class PlanIn(BaseModel):
    goal: str


@app.post("/api/plan")
def plan_endpoint(payload: PlanIn):
    plan = build_plan(payload.goal)
    return plan.model_dump()


@app.post("/api/plan/repair")
def plan_repair_endpoint(payload: dict):
    plan = repair_plan(payload)
    return plan.model_dump()
'''
    main_path.write_text(text.rstrip() + "\n" + addition)
    print("Planner routes were appended.")
else:
    print("Planner routes already present.")
"""
        ),
        acceptance(
            "curl -X POST http://localhost:8000/api/plan -H 'Content-Type: application/json' -d '{\"goal\":\"Build a demo\"}'",
            "A JSON object containing a goal and an ordered list of steps is returned.",
        ),
        homework([
            "Client-side rendering of planner steps is drafted for the frontend.",
            "Additional validation rules are explored for complex goals.",
        ]),
    ],
))

labs.append((
    "Lab05_Simple_Agent_and_Tools",
    "Lab 05 · Simple Agent and Tools",
    [
        md(
            """## Objectives
- A minimal agent loop is expressed with limited iterations.
- Tool abstractions for calculator, db_query, and search_faq are prepared.
- Tool call timelines are logged for review.
"""
        ),
        md(
            """## What will be learned
- Agent planning loops are reasoned about with deterministic stops.
- Tool registration strategies are documented.
- Logging of tool usage is practiced for observability.
"""
        ),
        md(
            """## Prerequisites & install
The following commands are intended for local execution.

```bash
cd ai-web/backend
. .venv/bin/activate
pip install numpy
```
"""
        ),
        md(
            """## Step-by-step tasks
### Step 1: Tool definitions
Lightweight tool functions are placed in a tools module.
"""
        ),
        code(
            """
from pathlib import Path
module = Path("ai-web/backend/app/tools.py")
module.write_text('''from typing import Any, Dict, List


TOOL_LOG: List[Dict[str, Any]] = []


def calculator(expression: str) -> str:
    TOOL_LOG.append({"tool": "calculator", "input": expression})
    try:
        value = eval(expression, {"__builtins__": {}}, {})
    except Exception:
        return "A calculation error was observed."
    return str(value)


def db_query(sql: str) -> str:
    TOOL_LOG.append({"tool": "db_query", "input": sql})
    return "A mock database response was produced."


def search_faq(question: str) -> str:
    TOOL_LOG.append({"tool": "search_faq", "input": question})
    return "A documented FAQ entry was suggested."
''')
print("Tools module was created.")
"""
        ),
        md(
            """### Step 2: Agent loop outline
A simple agent loop is introduced with a two-iteration limit.
"""
        ),
        code(
            """
from pathlib import Path
agent_path = Path("ai-web/backend/app/agent.py")
agent_path.write_text('''from typing import Dict, List

from .tools import TOOL_LOG, calculator, db_query, search_faq


def run_agent(task: str) -> Dict[str, List[str]]:
    TOOL_LOG.clear()
    thoughts = [f"The task was received: {task}"]
    for step in range(2):
        if "calculate" in task and step == 0:
            result = calculator("1 + 1")
            thoughts.append(f"Calculator returned {result}.")
        elif "database" in task and step == 0:
            result = db_query("SELECT * FROM items LIMIT 1")
            thoughts.append(result)
        else:
            result = search_faq(task)
            thoughts.append(result)
    timeline = [f"{entry['tool']} ← {entry['input']}" for entry in TOOL_LOG]
    return {"thoughts": thoughts, "timeline": timeline}
''')
print("Agent loop was documented.")
"""
        ),
        md(
            """### Step 3: Endpoint exposure
The agent run is exposed through FastAPI for easy testing.
"""
        ),
        code(
            """
from pathlib import Path
main_path = Path("ai-web/backend/app/main.py")
text = main_path.read_text()
if "agent_endpoint" not in text:
    addition = '''
from .agent import run_agent


@app.post("/api/agent")
def agent_endpoint(payload: dict):
    task = payload.get("task", "A task was not specified.")
    result = run_agent(task)
    return result
'''
    main_path.write_text(text.rstrip() + "\n" + addition)
    print("Agent endpoint was appended.")
else:
    print("Agent endpoint already present.")
"""
        ),
        acceptance(
            "curl -X POST http://localhost:8000/api/agent -H 'Content-Type: application/json' -d '{\"task\":\"calculate 1+1\"}'",
            "The response includes thoughts and a timeline reflecting tool usage.",
        ),
        homework([
            "Tool error handling pathways are drafted for robustness.",
            "Agent iteration limits are experimented with for longer plans.",
        ]),
    ],
))

labs.append((
    "Lab06_Embeddings_and_FAISS",
    "Lab 06 · Embeddings and FAISS",
    [
        md(
            """## Objectives
- Document chunking routines are introduced.
- The \"text-embedding-004\" vectors are stored in a FAISS index.
- A search endpoint returns top results with scores.
"""
        ),
        md(
            """## What will be learned
- Document preprocessing for embeddings is rehearsed.
- FAISS index persistence is described.
- Vector search endpoints are surfaced.
"""
        ),
        md(
            """## Prerequisites & install
The following commands are intended for local execution.

```bash
cd ai-web/backend
. .venv/bin/activate
pip install faiss-cpu google-generativeai numpy
```
"""
        ),
        md(
            """## Step-by-step tasks
### Step 1: Chunking utility
A chunking helper is added so documents are segmented.
"""
        ),
        code(
            """
from pathlib import Path
vector_path = Path("ai-web/backend/app/vector.py")
vector_path.write_text('''import json
import os
from pathlib import Path
from typing import List, Tuple

from google import genai
import numpy as np
import faiss


DATA_DIR = Path(__file__).resolve().parent / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
INDEX_FILE = DATA_DIR / "embeddings.index"
META_FILE = DATA_DIR / "metadata.json"


def _client() -> genai.Client:
  api_key = os.environ.get('GEMINI_API_KEY', '')
  if not api_key:
    raise RuntimeError('A backend API key is required for embeddings.')
  return genai.Client(api_key=api_key)


def _text_content(text: str) -> dict:
  return {"parts": [{"text": text}]}


def chunk_text(text: str, size: int = 400) -> List[str]:
  return [text[i:i + size] for i in range(0, len(text), size) if text[i:i + size].strip()]


def embed_chunks(chunks: List[str]) -> np.ndarray:
  client = _client()
  response = client.models.embed_content(
      model='text-embedding-004',
      contents=[_text_content(chunk) for chunk in chunks],
  )
  embeddings = response.embeddings or []
  if not embeddings:
    raise RuntimeError('No embeddings were returned from the Gemini API.')
  return np.array([item.values for item in embeddings], dtype=np.float32)


def save_index(chunks: List[str], vectors: np.ndarray) -> None:
  index = faiss.IndexFlatIP(vectors.shape[1])
  faiss.normalize_L2(vectors)
  index.add(vectors)
  faiss.write_index(index, str(INDEX_FILE))
  META_FILE.write_text(json.dumps({"chunks": chunks}))


def load_index() -> Tuple[faiss.Index, List[str]]:
  index = faiss.read_index(str(INDEX_FILE))
  chunks = json.loads(META_FILE.read_text())["chunks"]
  return index, chunks


def search(query: str, top_k: int = 3) -> List[Tuple[str, float]]:
  index, chunks = load_index()
  query_vec = embed_chunks([query])
  faiss.normalize_L2(query_vec)
  scores, neighbors = index.search(query_vec, top_k)
  return [(chunks[i], float(scores[0][pos])) for pos, i in enumerate(neighbors[0])]
''')
print("Vector helper was written.")
"""
        ),
        md(
            """### Step 2: Index builder cell
An index is created from a small sample document.
"""
        ),
        code(
            """
import sys
from pathlib import Path

sys.path.append(str(Path('ai-web/backend')))
from app.vector import chunk_text, embed_chunks, save_index

sample_text = "\"\"This course demonstrates AI in web programming.\nThe backend relies on FastAPI and Gemini proxies.\nVector search provides relevant snippets.\n\"\"\"
chunks = chunk_text(sample_text)
vectors = embed_chunks(chunks)
save_index(chunks, vectors)
print('Index was generated with', len(chunks), 'chunks.')
"""
        ),
        md(
            """### Step 3: Search endpoint
A FastAPI endpoint is published for vector search.
"""
        ),
        code(
            """
from pathlib import Path
main_path = Path("ai-web/backend/app/main.py")
text = main_path.read_text()
if "search_endpoint" not in text:
    addition = '''
from typing import Optional
from .vector import search


@app.get("/api/search")
def search_endpoint(q: str, k: Optional[int] = 3):
    results = search(q, int(k))
    return {"results": [{"text": text, "score": score} for text, score in results]}
'''
    main_path.write_text(text.rstrip() + "\n" + addition)
    print("Search endpoint was appended.")
else:
    print("Search endpoint already present.")
"""
        ),
        acceptance(
            "curl 'http://localhost:8000/api/search?q=fastapi&k=2'",
            "A JSON response containing scored chunks is observed.",
        ),
        homework([
            "Periodic index rebuild strategies are evaluated for large document sets.",
            "Client-side rendering of search results is explored.",
        ]),
    ],
))

labs.append((
    "Lab07_RAG_with_Citations",
    "Lab 07 · RAG with Citations",
    [
        md(
            """## Objectives
- Retrieved chunks are combined into grounded answers.
- Inline citation markers such as [S1] are emitted.
- Refusals are documented when no evidence is present.
"""
        ),
        md(
            """## What will be learned
- Response assembly with citations is structured.
- Evidence gating ensures unsupported answers are refused.
- Backend orchestration for RAG is reinforced.
"""
        ),
        md(
            """## Prerequisites & install
The following commands are intended for local execution.

```bash
cd ai-web/backend
. .venv/bin/activate
pip install google-generativeai
```
"""
        ),
        md(
            """## Step-by-step tasks
### Step 1: RAG helper
A helper combines retrieved chunks with a Gemini completion.
"""
        ),
        code(
            """
from pathlib import Path
rag_path = Path("ai-web/backend/app/rag.py")
rag_path.write_text('''from typing import List

from .vector import search
from .llm import chat


def answer(question: str) -> dict:
    retrieved = search(question, 3)
    if not retrieved:
        return {"answer": "No supported answer can be provided without evidence.", "chunks": []}
    citations = [f"[S{idx + 1}]" for idx in range(len(retrieved))]
    prompt = [
        {"role": "user", "content": f"Question: {question}. Use only the provided snippets."},
        {"role": "model", "content": "Sources:\n" + "\n".join(f"[S{idx + 1}] {text}" for idx, (text, _) in enumerate(retrieved))}
    ]
    completion = chat(prompt)
    return {"answer": completion, "chunks": [{"id": f"S{idx + 1}", "text": text, "score": score} for idx, (text, score) in enumerate(retrieved)], "citations": citations}
''')
print("RAG helper was created.")
"""
        ),
        md(
            """### Step 2: Endpoint exposure
The RAG helper is surfaced under /api/answer.
"""
        ),
        code(
            """
from pathlib import Path
main_path = Path("ai-web/backend/app/main.py")
text = main_path.read_text()
if "answer_endpoint" not in text:
    addition = '''
from .rag import answer as answer_question


@app.get("/api/answer")
def answer_endpoint(q: str):
    result = answer_question(q)
    if not result.get("chunks"):
        return {"answer": "No supported answer can be provided without evidence.", "citations": []}
    return result
'''
    main_path.write_text(text.rstrip() + "\n" + addition)
    print("Answer endpoint was appended.")
else:
    print("Answer endpoint already present.")
"""
        ),
        acceptance(
            "curl 'http://localhost:8000/api/answer?q=course goals'",
            "A cited answer referencing [S1] style markers is produced when evidence exists.",
        ),
        homework([
            "Citation rendering is enhanced in the frontend chat UI.",
            "Fallback messaging is drafted for unanswered questions.",
        ]),
    ],
))

labs.append((
    "Lab08_TensorFlowJS_Browser_Inference",
    "Lab 08 · TensorFlow.js Browser Inference",
    [
        md(
            """## Objectives
- TensorFlow.js is loaded in the browser for local inference.
- A webcam or file input is provided without backend calls.
- Prediction results are rendered with lightweight styling.
"""
        ),
        md(
            """## What will be learned
- Client-side model loading is rehearsed.
- User media APIs are reviewed for inference demos.
- Result presentation is refined for clarity.
"""
        ),
        md(
            """## Prerequisites & install
The following commands are intended for local execution.

```bash
cd ai-web/frontend
npm install @tensorflow/tfjs @tensorflow-models/coco-ssd
```
"""
        ),
        md(
            """## Step-by-step tasks
### Step 1: Component shell
A React component is outlined for TensorFlow.js usage.
"""
        ),
        code(
            """
from pathlib import Path
app_js = Path("ai-web/frontend/src/App.jsx")
app_js.write_text('''import React, { useEffect, useRef, useState } from 'react';
import * as cocoSsd from '@tensorflow-models/coco-ssd';
import '@tensorflow/tfjs';

function App() {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const [status, setStatus] = useState('Model is loading…');
  const [model, setModel] = useState(null);

  useEffect(() => {
    async function prepare() {
      try {
        const loaded = await cocoSsd.load();
        setModel(loaded);
        setStatus('Model is ready.');
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        if (videoRef.current) {
          videoRef.current.srcObject = stream;
        }
      } catch (error) {
        setStatus('Camera or model initialization failed.');
      }
    }
    prepare();
  }, []);

  async function handleDetect() {
    if (!model || !videoRef.current) {
      setStatus('Detection is unavailable at this time.');
      return;
    }
    const predictions = await model.detect(videoRef.current);
    const canvas = canvasRef.current;
    const context = canvas.getContext('2d');
    context.clearRect(0, 0, canvas.width, canvas.height);
    context.font = '16px sans-serif';
    predictions.forEach((prediction, index) => {
      context.fillText(`${index + 1}. ${prediction.class} (${prediction.score.toFixed(2)})`, 10, 20 + index * 18);
    });
    setStatus(`${predictions.length} objects were detected.`);
  }

  return (
    <main style={{ padding: 24 }}>
      <h1>Lab 8 — TensorFlow.js Inference</h1>
      <p>{status}</p>
      <video ref={videoRef} width={320} height={240} autoPlay playsInline muted />
      <canvas ref={canvasRef} width={320} height={240} style={{ border: '1px solid #ccc' }} />
      <button type="button" onClick={handleDetect}>Run detection</button>
    </main>
  );
}

export default App;
''')
print("TensorFlow.js demo was written.")
"""
        ),
        acceptance(
            "curl http://localhost:8000/health",
            "The backend health check remains accessible while the frontend serves the TensorFlow.js UI.",
        ),
        homework([
            "Image upload support is investigated for offline detection.",
            "Result overlays are explored to highlight detections on the video feed.",
        ]),
    ],
))

labs.append((
    "Lab09_Agent_Memory_SQLite",
    "Lab 09 · Agent Memory with SQLite",
    [
        md(
            """## Objectives
- A SQLite schema is designed for sessions, messages, and memories.
- A memory summarization plan is drafted for periodic runs.
- Data access helpers are introduced.
"""
        ),
        md(
            """## What will be learned
- SQLite migrations are sketched for conversational data.
- Summarization planning is discussed for memory consolidation.
- Repository patterns for data access are reinforced.
"""
        ),
        md(
            """## Prerequisites & install
The following commands are intended for local execution.

```bash
cd ai-web/backend
. .venv/bin/activate
pip install sqlite-utils
```
"""
        ),
        md(
            """## Step-by-step tasks
### Step 1: Schema file
A schema file is provided to capture sessions, messages, and memories.
"""
        ),
        code(
            """
from pathlib import Path
schema_path = Path("ai-web/backend/app/schema.sql")
schema_path.write_text('''CREATE TABLE IF NOT EXISTS sessions (
  id TEXT PRIMARY KEY,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS messages (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  session_id TEXT REFERENCES sessions(id),
  role TEXT,
  content TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS memories (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  session_id TEXT REFERENCES sessions(id),
  summary TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  next_review TIMESTAMP
);
''')
print("Schema file was produced.")
"""
        ),
        md(
            """### Step 2: Repository helper
A helper module is included for interacting with SQLite.
"""
        ),
        code(
            """
from pathlib import Path
repo_path = Path("ai-web/backend/app/repository.py")
repo_path.write_text('''import sqlite3
from pathlib import Path
from typing import Iterable

DB_PATH = Path(__file__).resolve().parent / "data.sqlite3"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def apply_schema(schema_sql: str):
    conn = get_connection()
    conn.executescript(schema_sql)
    conn.commit()
    conn.close()


def insert_message(session_id: str, role: str, content: str):
    conn = get_connection()
    conn.execute(
        "INSERT INTO messages (session_id, role, content) VALUES (?, ?, ?)",
        (session_id, role, content),
    )
    conn.commit()
    conn.close()


def list_recent_messages(session_id: str, limit: int = 10) -> Iterable[sqlite3.Row]:
    conn = get_connection()
    rows = conn.execute(
        "SELECT role, content FROM messages WHERE session_id = ? ORDER BY created_at DESC LIMIT ?",
        (session_id, limit),
    ).fetchall()
    conn.close()
    return rows
''')
print("Repository helper was created.")
"""
        ),
        md(
            """### Step 3: Summarization plan
A plan is described to summarize conversations periodically.
"""
        ),
        md(
            """A periodic job is proposed in which conversations are summarized into the memories table. The job is scheduled after a session surpasses a message threshold. A placeholder function is positioned so later labs can hook in summarization calls.
"""
        ),
        code(
            """
from pathlib import Path
plan_path = Path("ai-web/backend/app/memory_plan.py")
plan_path.write_text('''from datetime import datetime, timedelta


def plan_memory_summary(session_id: str) -> dict:
    return {
        "session_id": session_id,
        "next_review": (datetime.utcnow() + timedelta(hours=6)).isoformat(),
        "status": "A summarization run has been scheduled.",
    }
''')
print("Memory plan placeholder was drafted.")
"""
        ),
        acceptance(
            "curl http://localhost:8000/health",
            "The backend health endpoint remains operational after SQLite helpers are introduced.",
        ),
        homework([
            "A cron-style schedule is documented for invoking the summarization plan.",
            "Additional indexing strategies are explored for the messages table.",
        ]),
    ],
))

labs.append((
    "Lab10_Evaluation_Latency_Cache",
    "Lab 10 · Evaluation, Latency, and Cache",
    [
        md(
            """## Objectives
- A tiny evaluation set is logged for backend prompts.
- Latency and token usage metrics are recorded.
- A naive cache hashes prompt plus tool context.
"""
        ),
        md(
            """## What will be learned
- Evaluation harness design is reviewed for LLM flows.
- Latency tracking is reinforced with timestamp instrumentation.
- Cache strategies are described for simple reuse.
"""
        ),
        md(
            """## Prerequisites & install
The following commands are intended for local execution.

```bash
cd ai-web/backend
. .venv/bin/activate
pip install google-generativeai
```
"""
        ),
        md(
            """## Step-by-step tasks
### Step 1: Evaluation dataset stub
A small evaluation dataset is stored for reproducibility.
"""
        ),
        code(
            """
from pathlib import Path
fixture_path = Path("ai-web/backend/app/eval_set.json")
fixture_path.write_text('''[
  {"prompt": "Summarize the project goals.", "expected": "A concise description is returned."},
  {"prompt": "List backend components.", "expected": "FastAPI, FAISS, and Gemini proxy are noted."}
]
''')
print("Evaluation dataset was created.")
"""
        ),
        md(
            """### Step 2: Metrics helper
A helper is provided to time requests and count tokens.
"""
        ),
        code(
            """
from pathlib import Path
metrics_path = Path("ai-web/backend/app/metrics.py")
metrics_path.write_text('''import hashlib
import json
import time
from contextlib import contextmanager
from typing import Dict

TOKEN_LOG: Dict[str, int] = {}


@contextmanager
def track_latency(label: str):
    start = time.perf_counter()
    yield
    duration = time.perf_counter() - start
    print(f"{label} latency: {duration:.3f}s")


def cache_key(prompt: str, tools: str) -> str:
    payload = json.dumps({"prompt": prompt, "tools": tools}, sort_keys=True)
    return hashlib.sha256(payload.encode('utf-8')).hexdigest()


def record_tokens(label: str, count: int):
    TOKEN_LOG[label] = TOKEN_LOG.get(label, 0) + count
''')
print("Metrics helper was written.")
"""
        ),
        md(
            """### Step 3: Cache-enabled endpoint
An evaluation endpoint is instrumented with caching and latency tracking.
"""
        ),
        code(
            """
from pathlib import Path
main_path = Path("ai-web/backend/app/main.py")
text = main_path.read_text()
if "evaluation_endpoint" not in text:
    addition = '''
from .metrics import cache_key, record_tokens, track_latency
from .llm import chat as llm_chat

CACHE = {}


@app.post("/api/evaluate")
def evaluation_endpoint(payload: dict):
    prompt = payload.get("prompt", "")
    tools = "".join(payload.get("tools", []))
    key = cache_key(prompt, tools)
    if key in CACHE:
        return {"cached": True, "response": CACHE[key]}
    with track_latency("evaluation"):
        response = llm_chat([
            {"role": "user", "content": prompt}
        ])
    record_tokens("evaluation", len(prompt.split()))
    CACHE[key] = response
    return {"cached": False, "response": response}
'''
    main_path.write_text(text.rstrip() + "\n" + addition)
    print("Evaluation endpoint was appended.")
else:
    print("Evaluation endpoint already present.")
"""
        ),
        acceptance(
            "curl -X POST http://localhost:8000/api/evaluate -H 'Content-Type: application/json' -d '{\"prompt\":\"Summarize the project goals.\"}'",
            "Responses indicate whether cache hits occurred and include evaluation output.",
        ),
        homework([
            "Token accounting is integrated with external monitoring dashboards.",
            "Additional evaluation prompts are composed for regression coverage.",
        ]),
    ],
))

labs.append((
    "Lab11_Security_and_Hardening",
    "Lab 11 · Security and Hardening",
    [
        md(
            """## Objectives
- Production CORS settings are tightened.
- Payload limits and allow-lists are described.
- SlowAPI rate limiting and prompt-injection checklists are provided.
"""
        ),
        md(
            """## What will be learned
- Environment-specific CORS strategies are reinforced.
- Input validation patterns are documented for safety.
- Prompt-injection mitigations are rehearsed for RAG systems.
"""
        ),
        md(
            """## Prerequisites & install
The following commands are intended for local execution.

```bash
cd ai-web/backend
. .venv/bin/activate
pip install slowapi
```
"""
        ),
        md(
            """## Step-by-step tasks
### Step 1: Security settings module
Security utilities are collected for reuse.
"""
        ),
        code(
            """
from pathlib import Path
security_path = Path("ai-web/backend/app/security.py")
security_path.write_text('''from slowapi import Limiter
from slowapi.util import get_remote_address
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

SAFE_ORIGINS = ["https://example.com"]
ALLOWED_FILES = {".txt", ".md"}
limiter = Limiter(key_func=get_remote_address, default_limits=["60/minute"])


def configure_security(app: FastAPI):
    app.state.limiter = limiter
    app.add_middleware(
        CORSMiddleware,
        allow_origins=SAFE_ORIGINS,
        allow_credentials=True,
        allow_methods=["GET", "POST"],
        allow_headers=["Content-Type", "Authorization"],
    )
''')
print("Security module was written.")
"""
        ),
        md(
            """### Step 2: Payload guard
A payload guard demonstrates enforcing limits and allow-lists.
"""
        ),
        code(
            """
from pathlib import Path
limits_path = Path("ai-web/backend/app/guards.py")
limits_path.write_text('''from fastapi import HTTPException, UploadFile

MAX_PAYLOAD_BYTES = 1024 * 1024
ALLOWED_EXTENSIONS = {".txt", ".md", ".pdf"}


def enforce_size(data: bytes):
    if len(data) > MAX_PAYLOAD_BYTES:
        raise HTTPException(status_code=413, detail="Payload size limit was exceeded.")


def enforce_extension(upload: UploadFile):
    if not any(upload.filename.endswith(ext) for ext in ALLOWED_EXTENSIONS):
        raise HTTPException(status_code=400, detail="File extension was not allowed.")
''')
print("Payload guard was documented.")
"""
        ),
        md(
            """### Step 3: Prompt-injection checklist
A checklist is referenced for the RAG pipeline.
"""
        ),
        md(
            """A checklist is maintained:
- External instructions are screened for deny-list phrases.
- Citations are verified prior to response emission.
- Sensitive tools are disabled when citations are missing.
"""
        ),
        acceptance(
            "curl http://localhost:8000/health",
            "The hardened configuration preserves the health endpoint for monitoring.",
        ),
        homework([
            "Rate limiting thresholds are tuned for production traffic patterns.",
            "Security review notes are captured alongside deployment manifests.",
        ]),
    ],
))

labs.append((
    "Lab12_Deployment_and_Docker",
    "Lab 12 · Deployment and Docker",
    [
        md(
            """## Objectives
- A backend Dockerfile is drafted with environment configuration guidance.
- A docker-compose sketch is recorded for local orchestration.
- Frontend build and deployment checklists are enumerated.
"""
        ),
        md(
            """## What will be learned
- Containerization patterns are reviewed for FastAPI and React.
- Environment variable documentation is reinforced for deployment.
- Health check considerations are summarized for operations.
"""
        ),
        md(
            """## Prerequisites & install
The following commands are intended for local execution.

```bash
# Docker installation is confirmed locally
docker --version
docker compose version
```
"""
        ),
        md(
            """## Step-by-step tasks
### Step 1: Backend Dockerfile
A Dockerfile is created for the FastAPI backend.
"""
        ),
        code(
            """
from pathlib import Path
dockerfile_path = Path("ai-web/backend/Dockerfile")
dockerfile_path.write_text('''FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . ./
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
''')
print("Backend Dockerfile was created.")
"""
        ),
        md(
            """### Step 2: Compose sketch
A docker-compose.yml sketch references backend and frontend builds.
"""
        ),
        code(
            """
from pathlib import Path
compose_path = Path("ai-web/docker-compose.yml")
compose_path.write_text('''version: '3.9'
services:
  backend:
    build: ./backend
    environment:
      - GEMINI_API_KEY=${GEMINI_API_KEY}
    ports:
      - "8000:8000"
  frontend:
    build: ./frontend
    ports:
      - "5173:5173"
    environment:
      - VITE_API_BASE=http://localhost:8000
''')
print("Compose sketch was drafted.")
"""
        ),
        md(
            """### Step 3: Deployment checklist
Deployment steps are summarized for future reference.
"""
        ),
        md(
            """A deployment checklist is tracked:
- Environment files are reviewed and populated without committing secrets.
- docker compose build and docker compose up commands are executed locally for testing.
- Health checks are observed via /health before promoting changes.
- A demo script is outlined describing backend startup, frontend build, and proxy verification.
"""
        ),
        acceptance(
            "curl http://localhost:8000/health",
            "Container builds expose the health endpoint for readiness checks.",
        ),
        homework([
            "CI/CD pipeline steps are enumerated for automated deployments.",
            "Frontend build artifacts are hosted on a static site provider checklist.",
        ]),
    ],
))

for name, title, cells in labs:
    write_notebook(name, title, cells)

print("All notebooks were generated under ai-web/labs.")
