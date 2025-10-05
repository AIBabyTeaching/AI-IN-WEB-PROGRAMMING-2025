"""Echo-related API routes used throughout the web programming labs.

The router exposes the lab's simple `/echo` endpoint alongside a `/flaky-echo`
variant that intentionally fails a configurable number of times.  Keeping these
routes in a dedicated module mirrors the folder structure that students build in
Lab 01, where routers, services, and schemas live in their own packages.
"""

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel

from app.services.echo import EchoServiceError, get_echo_payload, get_flaky_echo_payload

router = APIRouter(tags=["echo"])


class EchoIn(BaseModel):
    """Pydantic model describing the request body submitted from the frontend."""

    msg: str


@router.post("/echo")
def echo(payload: EchoIn) -> dict[str, str]:
    """Return the payload unchanged so students can verify request plumbing."""

    return get_echo_payload(payload.msg)


@router.post("/flaky-echo")
def flaky_echo(payload: EchoIn, request: Request, failures: int = 1) -> dict[str, int | str]:
    """Simulate transient failures before eventually returning the echoed message.

    The router delegates the retry tracking to the service layer so the example
    mirrors the lab notes that encourage thin route handlers.
    """

    client_host = request.client.host if request.client else "unknown"

    try:
        return get_flaky_echo_payload(payload.msg, client_host, failures)
    except EchoServiceError as exc:  # Translate the domain error into an HTTP error.
        raise HTTPException(status_code=503, detail=str(exc)) from exc
