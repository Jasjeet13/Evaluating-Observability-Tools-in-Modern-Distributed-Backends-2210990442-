import os

import httpx
from fastapi import FastAPI, HTTPException
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

from lab.config import require_env
from lab.fault import apply_network_delay
from lab.telemetry import http_client, init_telemetry

shutdown = init_telemetry("order-service")

app = FastAPI(title="order-service")
FastAPIInstrumentor.instrument_app(app)

PAYMENT_URL = require_env("PAYMENT_SERVICE_URL")


@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}


@app.post("/orders")
async def create_order() -> dict:
    await apply_network_delay()
    async with http_client() as client:
        resp = await client.post(f"{PAYMENT_URL}/payments/charge")
        if resp.status_code >= 400:
            raise HTTPException(status_code=502, detail=resp.text)
        return {"order_id": "ord-1001", "payment": resp.status_code}


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", "8082"))
    uvicorn.run("services.order.main:app", host="0.0.0.0", port=port, log_level="info")
