import json
import logging
from collections.abc import Callable
from typing import TypeVar

from fastapi.encoders import jsonable_encoder
from redis import Redis
from redis.exceptions import RedisError

from app.core.config import settings


logger = logging.getLogger(__name__)
T = TypeVar("T")


def get_redis_client() -> Redis:
    return Redis.from_url(settings.redis_url, decode_responses=True)


def project_tasks_cache_key(project_id: int) -> str:
    return f"projects:{project_id}:tasks"


def get_or_set_json_cache(key: str, ttl_seconds: int, loader: Callable[[], T]) -> T:
    redis_client = get_redis_client()

    try:
        cached_value = redis_client.get(key)
    except RedisError as exc:
        logger.warning("Redis cache read failed for key=%s: %s", key, exc)
        return loader()

    if cached_value is not None:
        logger.info("Cache hit key=%s", key)
        return json.loads(cached_value)

    logger.info("Cache miss key=%s", key)
    value = loader()

    try:
        redis_client.setex(key, ttl_seconds, json.dumps(jsonable_encoder(value)))
    except RedisError as exc:
        logger.warning("Redis cache write failed for key=%s: %s", key, exc)

    return value


def delete_cache_key(key: str) -> None:
    try:
        get_redis_client().delete(key)
        logger.info("Cache invalidated key=%s", key)
    except RedisError as exc:
        logger.warning("Redis cache delete failed for key=%s: %s", key, exc)
