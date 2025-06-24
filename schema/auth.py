from pydantic import BaseModel, Field


class GoogleUserData(BaseModel):
    id: int
    email: str
    verified_email: bool = Field(alias='verified_email')
    name: str
    access_token: str
