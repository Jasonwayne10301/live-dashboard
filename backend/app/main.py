from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

from app.api.v1.router import api_router
from app.api.v1.endpoints import websocket
from app.core.config import settings
from app.core.simulator import MetricSimulator
from app.core.prometheus_metrics import cpu_gauge, memory_gauge, disk_gauge, network_in_gauge, network_out_gauge, request_rate_gauge, response_time_gauge, active_connections_gauge

simulator = MetricSimulator()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await simulator.start()
    yield
    await simulator.stop()


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=settings.DESCRIPTION,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_STR)
app.include_router(websocket.router)  # WebSocket routes at root level


@app.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.get("/", tags=["Health"])
async def root():
    return {"message": settings.PROJECT_NAME, "docs": "/docs"}


@app.get("/health", tags=["Health"])
async def health():
    return {"status": "healthy", "version": settings.VERSION}
