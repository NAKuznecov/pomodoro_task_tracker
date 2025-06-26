import json

from redis import Redis

from app.tasks.schema import STask


class CacheTask:
    def __init__(self, redis: Redis):
        self.redis = redis

    def get_tasks(self):
        with self.redis as redis:
            tasks_json = redis.lrange('tasks', 0, -1)
            return [STask.model_validate(json.loads(task)) for task in tasks_json]

    def set_tasks(self, tasks: list[STask]):
        tasks_json = [task.model_dump_json() for task in tasks]
        self.redis.lpush('tasks', *tasks_json)
