from functools import wraps

from fastapi.responses import JSONResponse


def EndpointOOF(func):
    @wraps(func)
    def sync_wrapper(*args, **kwargs):
        return JSONResponse(
            status_code=503,
            content={
                "error": True,
                "message": {"error": "Endpoint is currently out of service."},
            },
        )

    @wraps(func)
    async def async_wrapper(*args, **kwargs):
        return sync_wrapper(*args, **kwargs)

    return async_wrapper
