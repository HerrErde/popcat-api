from datetime import datetime

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

app = FastAPI()


async def error_status(request: Request, call_next):
    try:
        response = await call_next(request)
        if response.status_code == 404:
            raise HTTPException(status_code=404)
        return response
    except HTTPException as exc:
        if exc.status_code == 404:
            return JSONResponse(
                status_code=exc.status_code,
                content={
                    "status": exc.status_code,
                    "error": {
                        "message": f"🔍 - Not Found - {request.url.path}",
                        "isError": True,
                    },
                    "dev": {
                        "stack": "👻",
                        "time": datetime.now().strftime("%m/%d/%Y | %I:%M:%S %p"),
                    },
                },
            )
        else:
            return JSONResponse(
                status_code=exc.status_code,
                content={
                    "status": exc.status_code,
                    "error": {
                        "message": "An error occurred",
                    },
                },
            )


# changes "detail" to "error" key
async def http_exception_handler(request, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content={"error": exc.detail})
