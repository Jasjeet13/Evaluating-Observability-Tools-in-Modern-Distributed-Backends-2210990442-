import asyncio
import os

from fastapi import FastAPI
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

from lab.fault import DelayMiddleware
from lab.telemetry import init_telemetry

shutdown = init_telemetry("payment-service")

app = FastAPI(title="payment-service")
app.add_middleware(DelayMiddleware, env_key="FAULT_DELAY_MS")
FastAPIInstrumentor.instrument_app(app)


@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}


@app.post("/payments/charge")
async def charge() -> dict:
    await asyncio.sleep(0.005)
    return {"status": "charged", "payment_id": "pay-9001"}


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", "8083"))
    delay = os.getenv("FAULT_DELAY_MS", "0")
    print(f"payment-service FAULT_DELAY_MS={delay}")
    uvicorn.run("services.payment.main:app", host="0.0.0.0", port=port, log_level="info")
