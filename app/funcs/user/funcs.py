# coding=utf-8

from datetime import datetime, timedelta, UTC
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jwt import encode, PyJWTError, decode

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from passlib.context import CryptContext

from app.models import User
from app.db import get_session
from app.conf import (
    SECRET_KEY,
    ALGORITHM,
    REFRESH_TOKEN_EXPIRE_MINUTES,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)


# Create an instance of CryptContext for password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# OAuth2PasswordBearer defines the token location for FastAPI
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


async def get_user_id(
        db_session: AsyncSession = Depends(get_session),
        token: str = Depends(oauth2_scheme)
) -> int:
    """
    Function to retrieve the current user's login from the JWT token.

    Decodes the JWT and returns the login from the "sub" field.
    This function is used as a dependency to check if the user is authenticated.

    Args:
        db_session (AsyncSession): Database session for interacting with the database.
        token: JWT token provided in the request.

    Raises:
        HTTPException: If the token is invalid or expired.

    Returns:
        int: The Id of the authenticated user.
    """

    # Defined credentials exception
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Decode the JWT token and get login
        payload = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        login: str = payload.get("sub")

        if login is None:
            # Not found
            raise credentials_exception

        # Check user
        user: User | None = await db_session.scalar(
            select(
                User
            ).where(
                (
                    User.login == login
                )
            )
        )

        if not user:
            # Exist user
            raise credentials_exception

        return user.id

    except PyJWTError:
        # Error
        raise credentials_exception


def create_token(
        login: str,
        expires_delta: int | None = 30
) -> str:
    """
    Function to create a JWT token with an expiration time.

    Args:
        login (str): The unique identifier for the user (typically the user's login).
        expires_delta (int | None): The expiration time of the token in minutes.

    Returns:
        str: The generated JWT token, encoded with the user's login and expiration time.
    """

    # Defined expire time
    expire_time = datetime.now(UTC) + timedelta(minutes=int(expires_delta))

    # Defined encode value
    encode_value = {
        "sub": login,
        "exp": expire_time
    }

    # Encode the data into a JWT token
    encoded_jwt = encode(encode_value, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


async def create_user(
        db_session: AsyncSession,
        first_name: str,
        last_name: str,
        login: str,
        password: str,
) -> User:
    """
    Function to create a new user in the database.

    Args:
        db_session (AsyncSession): The database session used to interact with the database.
        first_name (str): The first name of the user.
        last_name (str): The last name of the user.
        login (str): The unique login (username) for the user.
        password (str): The plain password provided by the user.

    Raises:
        HTTPException: If the user already exists with the provided login.

    Returns:
        User: The newly created user object with the hashed password stored.
    """

    # Check user
    user: User | None = await db_session.scalar(
        select(
            User
        ).where(
            (
                User.login == login
            )
        )
    )

    if user:
        # Exist user
        raise HTTPException(
            status_code=400,
            detail="User already with this login registered"
        )

    # Hash the password
    hashed_password = pwd_context.hash(password)

    # Create a new user
    new_user = User(
        first_name=first_name,
        last_name=last_name,
        login=login,
        hashed_password=hashed_password
    )

    # Save all changes
    db_session.add(new_user)
    await db_session.commit()
    await db_session.refresh(new_user)

    return new_user


async def login_user(
        db_session: AsyncSession,
        login: str,
        password: str
) -> dict:
    """
    Authenticates a user based on login and password, and generates JWT tokens (access & refresh) upon successful login.

    Args:
        db_session (AsyncSession): The database session used to interact with the database asynchronously.
        login (str): The user's login (username) to identify the user.
        password (str): The user's password to verify the user's identity.

    Raises:
        HTTPException: If the user is not found or the password is incorrect, raises a 401 Unauthorized error.

    Returns:
        dict: A dictionary containing the access token, refresh token, and token type.
    """

    # Get user from DB
    result = await db_session.execute(select(User).filter(User.login == login))
    db_user = result.scalars().first()

    if db_user is None or not pwd_context.verify(password, db_user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    # Generate access and refresh tokens
    access_token = create_token(login=login, expires_delta=ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token = create_token(login=login, expires_delta=REFRESH_TOKEN_EXPIRE_MINUTES)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }
