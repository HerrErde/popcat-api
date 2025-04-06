from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from config import config
from helper import RedisHandler, error_status
from route.route import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await RedisHandler().initialize()
    yield


app = FastAPI(
    debug=config.debug,
    title="Pop Cat API",
    summary="List of all available endpoints in the Pop Cat API",
    openapi_url="/openapi.json",
    servers=[{"url": "https://api.popcat.xyz"}],
    docs_url="/api-docs",
    redoc_url=None,
    lifespan=lifespan,  # Add the lifespan context manager
)

# Include routers
app.include_router(router)

# Adding middleware
# app.middleware("http")(log_requests)
# app.middleware("http")(request_count)
app.middleware("http")(error_status)
# app.middleware("http")(http_exception_handler)


startargs = {"host": config.host, "port": config.port, "reload": config.debug}

if __name__ == "__main__":
    uvicorn.run("main:app", **startargs)
