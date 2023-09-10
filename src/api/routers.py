import hashlib

import aioboto3

from fastapi import APIRouter, Depends, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.session import get_db_connection
from src.api.models import ShowSplit, AudioFile
from src.aws.s3_maganer import S3Manager

from src.audio_processing import audio_splitter


split_router = APIRouter()


async def _make_split(file) -> ShowSplit:
    file_bytes = await file.read()
    audio_channels = await audio_splitter.split_audio(file_bytes)

    file_hash = hashlib.sha256(file_bytes).hexdigest()
    extension = file.filename.split('.')[-1]
    async with aioboto3.Session().client('s3') as s3_client:
        bucket_manager = S3Manager(s3_client)
        await bucket_manager.create_bucket()
        s3_urls = []
        for channel_number, channel in enumerate(audio_channels):
            s3_urls.append(await bucket_manager.upload_audio(channel, file_hash, channel_number, extension))


@split_router.post("/")
# db: AsyncSession = Depends(get_db_connection)
async def split_audio(file: UploadFile):
    return await _make_split(file)
