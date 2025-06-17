from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    sqllite_db: str = 'pomodoro.db'




