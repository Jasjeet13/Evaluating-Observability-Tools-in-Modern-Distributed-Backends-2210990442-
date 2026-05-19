import os

from fastapi import FastAPI
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

from lab.telemetry import init_telemetry

shutdown = init_telemetry("user-service")

app = FastAPI(title="user-service")
FastAPIInstrumentor.instrument_app(app)


@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}


@app.get("/users/{user_id}")
async def get_user(user_id: str) -> dict:
    return {"id": user_id, "name": "demo-user"}


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", "8081"))
    uvicorn.run("services.user.main:app", host="0.0.0.0", port=port, log_level="info")
