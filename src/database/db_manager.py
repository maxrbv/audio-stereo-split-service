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

    async def create_empty_file_info(self):
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

    async def add_request_info(self, audio_file_id: int):
        """
        Add a RequestHistory record with the given audio_file_id

        :param audio_file_id: The ID of the audio file associated with the request
        """
        try:
            request_info = RequestHistory(audio_file_id=audio_file_id)
            self.cur_session.add(request_info)
            await self.cur_session.commit()
        except Exception as e:
            await self.cur_session.rollback()
            raise e
