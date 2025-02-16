# coding=utf-8

from datetime import datetime

from pydantic import Field, BaseModel

from app.validation import ValidationValue


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
        min_length=ValidationValue.login_min_length,
        max_length=ValidationValue.login_max_length,
        pattern=ValidationValue.login_regex,
    )


class UserRequestRegisterSchema(UserSchema):
    password: str = Field(
        ...,
        example="1111111111",
        description="The plain password provided by the user. It will be hashed before storing.",
        min_length=ValidationValue.password_min_length,
        max_length=ValidationValue.password_max_length,
        pattern=ValidationValue.password_regex,
    )

    class Config:
        extra = "forbid"


class UserResponseRegisterSchema(UserSchema):
    created_at: datetime = Field(
        ...,
        description="The timestamp when the user account was created.",
    )

    class Config:
        from_attributes = True


class UserRequestLoginSchema(BaseModel):
    login: str = Field(
        ...,
        example="wheel_smet",
        description="The unique login (username) for the user.",
        min_length=ValidationValue.login_min_length,
        max_length=ValidationValue.login_max_length,
        pattern=ValidationValue.login_regex,
    )
    password: str = Field(
        ...,
        example="1111111111",
        description="The plain password provided by the user. It will be hashed before storing.",
        min_length=ValidationValue.password_min_length,
        max_length=ValidationValue.password_max_length,
        pattern=ValidationValue.password_regex,
    )

    class Config:
        extra = "forbid"


class UserResponseLoginSchema(BaseModel):
    token_type: str = Field(
        ...,
        example="bearer",
        description="The type of token."
    )
    access_token: str = Field(
        ...,
        example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJqb2huZG9lIiwiaWF0IjoxNjEyMzQ1Njc4fQ.Dk69",
        description=(
            "The JWT access token generated after successful authentication."
            " This token is used for accessing protected resources in the API."
            " It contains user identification and an expiration time."
        ),
    )
