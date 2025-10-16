from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.openapi.utils import get_openapi
from app.utils.logger import logger
from app.routers import generic

app = FastAPI(
    title="SDM Proxy API",
    description="Bridge pre Broadcom CA Service Desk Manager (SDM 17.4)",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(generic.router)


@app.get("/api/health", tags=["system"])
async def health_basic():
    return {"status": "ok", "service": "sdmproxy"}


@app.get("/api/health/full", tags=["system"])
async def health_full():
    return {"status": "ok", "version": "1.0.0", "service": "sdmproxy"}


@app.get("/openapi.json", include_in_schema=False)
async def get_openapi_spec():
    schema = get_openapi(
        title="SDM Proxy API",
        version="1.0.0",
        description="Bridge pre Broadcom CA SDM 17.4",
        routes=app.routes,
    )
    return JSONResponse(schema)


@app.get("/", include_in_schema=False)
async def root_redirect():
    return JSONResponse({"message": "SDM Proxy API running", "health": "/api/health"})
