import redis

def get_redis_connection() -> redis.Redis:
    return redis.Redis(host='0.0.0.0', port=6379, db=0)

