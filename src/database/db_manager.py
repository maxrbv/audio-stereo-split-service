from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from .models import Base, RequestHistory, FilesInfo


class DBManager:
    def __init__(self, database_url: str):
        self.database_url = database_url
        self.engine = create_async_engine(url=database_url, future=True, echo=False)
        self.session_factory = sessionmaker(self.engine, expire_on_commit=False, class_=AsyncSession)
        self.cur_session = None

    async def init_models(self):
        """
        Initialize database models and create tables if they don't exist
        """
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all, checkfirst=True)

    async def init(self):
        """
        Initialize the DBManager and create a session
        """
        self.cur_session = self.session_factory()
        await self.init_models()

    async def close(self):
        """
        Close the database connection and dispose of the engine
        """
        await self.engine.dispose()

    async def create_empty_file_info(self) -> int:
        """
        Create an empty FilesInfo record in the database and return its ID

        :return: The ID of the created FilesInfo record
        """
        try:
            file_info = FilesInfo()
            self.cur_session.add(file_info)
            await self.cur_session.commit()

            return file_info.id
        except Exception as e:
            await self.cur_session.rollback()
            raise e

    async def update_file_info(self, file_id: int, s3_url_1: str, s3_url_2: str):
        """
        Update the FilesInfo record with the given file ID with new S3 URLs

        :param file_id: The ID of the FilesInfo record to update
        :param s3_url_1: The first S3 URL to update
        :param s3_url_2: The second S3 URL to update
        """
        try:
            # Fetch the file record by file_id
            file_info = await self.cur_session.get(FilesInfo, file_id)

            # Update the file information
            if file_info:
                file_info.s3_url_1 = s3_url_1
                file_info.s3_url_2 = s3_url_2

            await self.cur_session.commit()
        except Exception as e:
            await self.cur_session.rollback()
            raise e

    async def add_request_info(self, audio_hash: str, audio_file_id: int):
        """
        Add a RequestHistory record with the given audio_file_id

        :param audio_hash: The hash of the audio file associated with the request
        :param audio_file_id: The ID of the audio file associated with the request
        """
        try:
            request_info = RequestHistory(audio_hash=audio_hash, audio_file_id=audio_file_id)
            self.cur_session.add(request_info)
            await self.cur_session.commit()
        except Exception as e:
            await self.cur_session.rollback()
            raise e

    async def get_urls_by_id(self, file_id: int) -> tuple[str, str]:
        """
        Retrieve S3 URLs by file ID from the database

        :param file_id: The ID of the file to retrieve S3 URLs for
        :return: A tuple containing two S3 URLs (s3_url_1 and s3_url_2)
        """
        try:
            # Fetch the file record by file_id
            file_info = await self.cur_session.get(FilesInfo, file_id)

            if file_info:
                return file_info.s3_url_1, file_info.s3_url_2

            # If the file is not found, raise an HTTPException with a 404 status code
            raise HTTPException(status_code=404, detail=f"File with ID {file_id} not found")
        except Exception as e:
            await self.cur_session.rollback()
            raise e

    async def get_id_by_hash(self, file_hash: str) -> int | None:
        """
        Retrieve the audio file ID associated with a given file hash from the database

        :param file_hash: The hash of the file for which to retrieve the audio file ID
        :return: The audio file ID if the hash is found in the database, or None if not found
        """
        try:
            # Create a select statement to retrieve the audio_file_id by audio_hash
            stmt = select(RequestHistory.audio_file_id).where(RequestHistory.audio_hash == file_hash)

            # Execute the query using the AsyncSession's execute method
            result = await self.cur_session.execute(stmt)

            # Fetch the first result row
            row = result.fetchone()

            if row:
                # If a matching record is found, return the associated audio file ID
                return row[0]
        except Exception as e:
            await self.cur_session.rollback()
            raise e
