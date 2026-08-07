from fastapi import APIRouter
import os
import time

router = APIRouter()

START_TIME = time.time()


@router.get("/health")
async def health_check():
    return {
        "status": "online",
        "agent": "ORION-Lite",
        "service": "health-api",
        "uptime_seconds": int(time.time() - START_TIME),
        "pid": os.getpid()
    }
