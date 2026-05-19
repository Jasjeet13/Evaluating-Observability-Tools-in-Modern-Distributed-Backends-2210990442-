import os

from fastapi import FastAPI, Response
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

from lab.config import require_env
from lab.telemetry import http_client, init_telemetry

shutdown = init_telemetry("api-gateway")

app = FastAPI(title="api-gateway")
FastAPIInstrumentor.instrument_app(app)

USER_URL = require_env("USER_SERVICE_URL")
ORDER_URL = require_env("ORDER_SERVICE_URL")


@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}


@app.post("/api/checkout")
async def checkout() -> Response:
    async with http_client() as client:
        u = await client.get(f"{USER_URL}/users/u1")
        if u.status_code >= 400:
            return Response(content=u.text, status_code=502)

        o = await client.post(f"{ORDER_URL}/orders")
        return Response(content=o.content, status_code=o.status_code, media_type="application/json")


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", "8080"))
    uvicorn.run("services.gateway.main:app", host="0.0.0.0", port=port, log_level="info")
