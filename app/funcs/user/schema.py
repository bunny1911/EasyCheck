# coding=utf-8

from datetime import datetime

from pydantic import BaseModel, Field


class UserSchema(BaseModel):
    first_name: str = Field(
        ...,
        example="Wheel",
        description="The first name of the user.",
    )
    last_name: str = Field(
        ...,
        example="Smet",
        description="The last name of the user.",
    )
    login: str = Field(
        ...,
        example="wheel_smet",
        description="The unique login (username) for the user.",
    )
    created_at: datetime | None = Field(
        default=None,
        description="The timestamp when the user account was created.",
        exclude=True,
    )

    class Config:
        orm_mode = True
