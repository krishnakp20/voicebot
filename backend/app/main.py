import logging

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.database import Base, engine
from app.middleware.logging import RequestLoggingMiddleware
import app.models  # noqa: F401
from app.routers import agents, auth, billing, calls, clients, dashboard, reports

app = FastAPI(title="Voice SaaS Platform", version="1.0.0")
logging.basicConfig(level=logging.INFO)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(RequestLoggingMiddleware)


@app.on_event("startup")
def startup() -> None:
    Base.metadata.create_all(bind=engine)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.exception_handler(Exception)
async def unhandled_exception(_: Request, exc: Exception):
    logging.exception("Unhandled exception: %s", exc)
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})


app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(clients.router, prefix="/clients", tags=["clients"])
app.include_router(agents.router, prefix="/agents", tags=["agents"])
app.include_router(calls.router, prefix="/calls", tags=["calls"])
app.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
app.include_router(billing.router, prefix="/billing", tags=["billing"])
app.include_router(reports.router, prefix="/reports", tags=["reports"])
