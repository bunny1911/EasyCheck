# coding=utf-8

from datetime import datetime

from pydantic import Field, BaseModel

from app.validation import ValidationValue


class UserSchema(BaseModel):
    first_name: str = Field(
        ...,
        examples=["Wheel"],
        description="The first name of the user.",
        pattern=ValidationValue.user_regex,
        min_length=ValidationValue.user_min_length,
    )
    last_name: str = Field(
        ...,
        examples=["Smet"],
        description="The last name of the user.",
        pattern=ValidationValue.user_regex,
        min_length=ValidationValue.user_min_length,
    )
    login: str = Field(
        ...,
        examples=["wheel_smet"],
        description="The unique login (username) for the user.",
        min_length=ValidationValue.login_min_length,
        max_length=ValidationValue.login_max_length,
        pattern=ValidationValue.login_regex,
    )


class UserRequestRegisterSchema(UserSchema):
    password: str = Field(
        ...,
        examples=["1111111111"],
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
        examples=["wheel_smet"],
        description="The unique login (username) for the user.",
        min_length=ValidationValue.login_min_length,
        max_length=ValidationValue.login_max_length,
        pattern=ValidationValue.login_regex,
    )
    password: str = Field(
        ...,
        examples=["1111111111"],
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
        examples=["bearer"],
        description="The type of token."
    )
    access_token: str = Field(
        ...,
        examples=["eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJqb2huZG9lIiwiaWF0IjoxNjEyMzQ1Njc4fQ.Dk69"],
        description=(
            "The JWT access token generated after successful authentication."
            " This token is used for accessing protected resources in the API."
            " It contains user identification and an expiration time."
        ),
    )
