# coding=utf-8

from datetime import datetime

from pydantic import Field, BaseModel


class UserRequestRegisterSchema(BaseModel):
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
    password: str = Field(
        ...,
        example="1111111111",
        description="The plain password provided by the user. It will be hashed before storing.",
    )


class UserResponseRegisterSchema(BaseModel):
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


class UserRequestLoginSchema(BaseModel):
    login: str = Field(
        ...,
        example="wheel_smet",
        description="The unique login (username) for the user.",
    )
    password: str = Field(
        ...,
        example="1111111111",
        description="The plain password provided by the user. It will be hashed before storing.",
    )


class UserResponseLoginSchema(BaseModel):
    access_token: str = Field(
        ...,
        example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJqb2huZG9lIiwiaWF0IjoxNjEyMzQ1Njc4fQ.Dk69",
        description=(
            "The JWT access token generated after successful authentication."
            " This token is used for accessing protected resources in the API."
            " It contains user identification and an expiration time."
        ),
    )
