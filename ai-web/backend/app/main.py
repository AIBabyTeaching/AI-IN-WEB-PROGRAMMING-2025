"""FastAPI application entry point used by the lab backend container."""

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.echo import router as echo_router
from app.routers.gemini import router as gemini_router

# Load environment variables from a local .env file when present so the
# application picks up credentials configured for the labs.
load_dotenv()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(echo_router)
app.include_router(gemini_router)


@app.get("/health")
def health() -> dict[str, str]:
    """Report service status for lab curl checks and container health probes."""

    return {"status": "ok"}
