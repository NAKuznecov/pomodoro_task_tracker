from multiprocessing.managers import Value

from pydantic import BaseModel, Field, model_validator


class STask(BaseModel):
    id: int
    name: str | None = None
    pomodoro_count: int | None = None
    category_id: int

    class Config:
        from_attributes = True


    @model_validator(mode='after')
    def check_name_or_pomodoro_count_is_not_none(self):
        if self.name is None and self.pomodoro_count is None:
            raise ValueError("Name or pomodoro count is None")
        return self