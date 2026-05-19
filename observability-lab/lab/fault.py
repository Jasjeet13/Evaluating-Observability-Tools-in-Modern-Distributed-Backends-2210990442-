import asyncio
import os
from typing import Awaitable, Callable

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response


def _delay_ms(env_key: str) -> int:
    raw = os.getenv(env_key, "0")
    try:
        return max(0, int(raw))
    except ValueError:
        return 0


class DelayMiddleware(BaseHTTPMiddleware):
    """Scenario S2: sleep before handling request (payment delay)."""

    def __init__(self, app, env_key: str = "FAULT_DELAY_MS"):
        super().__init__(app)
        self._delay_ms = _delay_ms(env_key)

    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
        if self._delay_ms > 0:
            await asyncio.sleep(self._delay_ms / 1000.0)
        return await call_next(request)


async def apply_network_delay() -> None:
    """Scenario S3: delay before outbound HTTP from order → payment."""
    ms = _delay_ms("FAULT_NETWORK_DELAY_MS")
    if ms > 0:
        await asyncio.sleep(ms / 1000.0)
