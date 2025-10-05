"""Service helpers containing the business logic for the echo endpoints.

The routers import these helpers so that the FastAPI layer remains focused on
HTTP details while the service layer owns the stateful retry simulation.  This
matches the separation of concerns demonstrated in the accompanying lab
notebooks and gives instructors a concrete example to reference in class.
"""

from dataclasses import dataclass


class EchoServiceError(RuntimeError):
    """Raised when the flaky echo service needs to signal a transient failure."""


@dataclass
class _FlakyState:
    """Internal data structure to keep track of how many failures each client saw."""

    attempts: int = 0


# Module-level dictionary storing retry counts keyed by client identifier.
_FLAKY_ATTEMPTS: dict[str, _FlakyState] = {}


def get_echo_payload(message: str) -> dict[str, str]:
    """Return the provided message wrapped in a JSON-friendly structure."""

    return {"msg": message}


def get_flaky_echo_payload(message: str, client_host: str, failures: int) -> dict[str, int | str]:
    """Return the echoed message, simulating transient errors on earlier attempts.

    Args:
        message: The string submitted from the frontend form.
        client_host: A stable identifier for the caller so each student sees their
            own retry counter.
        failures: The number of sequential failures to simulate before success.

    Raises:
        EchoServiceError: If the simulated service is still within the failure
            window and needs the client to retry.
    """

    key = f"{client_host}:{failures}"
    state = _FLAKY_ATTEMPTS.setdefault(key, _FlakyState())

    if state.attempts < failures:
        state.attempts += 1
        raise EchoServiceError("Simulated transient failure")

    attempts = state.attempts + 1  # Count the successful request as an attempt.
    _FLAKY_ATTEMPTS[key] = _FlakyState()  # Reset tracking for the next exercise run.

    return {"msg": message, "attempts": attempts}
