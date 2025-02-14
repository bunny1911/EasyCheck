# coding=utf-8

from fastapi import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext

from ..models import User

# Create an instance of CryptContext for password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


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
    db_user = await db_session.execute(
        db_session.query(User).filter(User.login == login)
    )
    db_user = db_user.first()

    if db_user:
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
