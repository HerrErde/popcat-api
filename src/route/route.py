from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse

from route import img_router, misc_router, text_router

router = APIRouter()


router.include_router(img_router)
router.include_router(text_router)
router.include_router(misc_router)


""" @router.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("assets/img/favicon.ico") """


@router.get("/", include_in_schema=False)
async def index_endpoint(request: Request):
    user_agent = request.headers.get("user-agent", "").lower()

    if user_agent != "":
        return RedirectResponse(
            "https://github.com/herrerde/popcat-api", status_code=308
        )
    else:
        return {"message": "Nothing here"}


@router.get("/endpoints")
async def endpoints_endpoint():
    routes = []
    for route in router.routes:
        route_info = {
            "methods": route.methods,
            "path": route.path,
            "name": route.name,
        }
        routes.append(route_info)
    return {"endpoints": routes}
