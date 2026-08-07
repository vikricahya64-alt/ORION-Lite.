from fastapi import FastAPI
from app.api.health import router as health_router


app = FastAPI(
    title="ORION-Lite API",
    version="1.0"
)


app.include_router(health_router)


@app.get("/")
async def root():
    return {
        "name": "ORION-Lite",
        "status": "running"
    }
