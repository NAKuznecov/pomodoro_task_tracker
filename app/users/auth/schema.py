from typing import Optional

from pydantic import BaseModel, Field


class UserLoginSchema(BaseModel):
    user_id: int
    access_token: str


class GoogleUserData(BaseModel):
    id: int = Field(..., alias="_id")
    email: str = Field(..., alias="email")
    verified_email: bool = Field(alias='verified_email')
    name: str = Field(..., alias='name')
    access_token: str = Field(..., alias='access_token')


class YandexUserData(BaseModel):
    id: int
    login: str
    name: str = Field(alias='real_name')
    default_email: str
    access_token: str
