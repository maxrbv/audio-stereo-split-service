from typing import Generator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

from src.settings import DATABASE_URL

# Create async engine for interaction with database
engine = create_async_engine(
    url=DATABASE_URL,
    future=True,
    echo=True,
)

# Create session for the interaction with database
async_session = sessionmaker(
    engine=engine,
    expire_on_commit=False,
    class_=AsyncSession,
)


async def get_db_connection() -> Generator:
    """
    Asynchronous context manager to obtain a database session

    :return: An asynchronous database session
    """
    session: AsyncSession | None = None
    try:
        session = async_session()
        yield session
    except SQLAlchemyError as e:
        print(f"Error initializing session: {e}")
        raise e
    finally:
        if session is not None:
            await session.close()
