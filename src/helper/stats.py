import threading
from datetime import datetime

from fastapi import Request

from helper.cache import RedisHandler

counter = 0
lock = threading.Lock()


async def request_count(request: Request, call_next):
    global counter

    redis_client = await RedisHandler().get_client()

    path = str(request.url.path)

    with lock:
        counter += 1

    try:
        key = f"stats:{path}"
        await redis_client.hincrby(key, "count", 1)
        await redis_client.hset(key, "last_request", datetime.now().isoformat())
    except Exception as e:
        print(f"Error updating Redis: {e}")

    response = await call_next(request)
    return response


"""
endpoint_stats = defaultdict(int)


@app.middleware("http")
async def count_endpoint_calls(request: Request, call_next):
    path = request.url.path
    name = request.scope.get("endpoint").__name__
    if path not in ["/stats"]:  # Exclude specific paths from being tracked
        endpoint_stats[name] += 1
    response = await call_next(request)
    return response


def custom_increment(endpoint_name: str):
    def dependency():
        endpoint_stats[endpoint_name] += 1

    return dependency


@app.get("/stats")
def get_stats():
    return {"endpoint_calls": dict(endpoint_stats)}


# Dictionary to store endpoint call counts
endpoint_stats = defaultdict(int)


@app.middleware("http")
async def count_endpoint_calls(request: Request, call_next):
    path = request.url.path
    endpoint_stats[path] += 1  # Increment the count for the requested endpoint
    response = await call_next(request)
    return response
"""
