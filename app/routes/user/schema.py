# coding=utf-8

from pydantic import Field

from app.funcs.user.schema import UserSchema


class UserResponseSchema(UserSchema):
    password: str = Field(
        ...,
        example="1111111111",
        description="The plain password provided by the user. It will be hashed before storing.",
        exclude=True,
    )
