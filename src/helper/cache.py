import redis.asyncio as redis

from config import config

redis_host = config.redis_host
redis_port = config.redis_port
redis_user = config.redis_user
redis_pass = config.redis_pass

REDIS_URI = f"redis://{redis_user}:{redis_pass}@{redis_host}:{redis_port}"


class RedisHandler:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RedisHandler, cls).__new__(cls)
            cls._instance._initialized = False
            cls._instance.redis_client = None
        return cls._instance

    async def initialize(self):
        if not self._initialized:
            self.redis_client = await redis.from_url(
                REDIS_URI, socket_timeout=5  # Use config.REDIS_URI directly
            )
            try:
                # Test connection
                await self.redis_client.ping()
                print("Successfully connected to Redis.")
                self._initialized = True
            except redis.ConnectionError as e:
                print(f"Redis ConnectionError: {e}")
            except redis.TimeoutError as e:
                print(f"Redis TimeoutError: {e}")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")

    async def get_client(self):
        if not self._initialized:
            await self.initialize()
        return self.redis_client
