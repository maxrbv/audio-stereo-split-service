import hashlib

from fastapi import APIRouter, UploadFile, HTTPException

from api.models import ShowFileID, ShowSplitURL
from initialize import db_manager, rabbitmq


split_router = APIRouter()


# Function to add the file data to the message queue
async def __add_to_queue(file_bytes: bytes, filename: str, file_id: int):
    await rabbitmq.publish(file_bytes, filename, file_id)


# Internal function to handle file splitting and processing
async def _make_split(file: UploadFile) -> ShowFileID:
    # Check if the file is an audio file based on its MIME type
    if not file.content_type.startswith('audio'):
        raise HTTPException(status_code=400, detail="Uploaded file is not an audio file.")

    # Read the uploaded file's bytes
    file_bytes = await file.read()
    filename = file.filename

    # Calculate the hash of the file's content
    file_hash = hashlib.sha256(file_bytes).hexdigest()

    # Check if the file with the same hash exists in the database
    file_id = await db_manager.get_id_by_hash(file_hash)
    if file_id:
        # If the file with the same hash exists, return its ID
        return ShowFileID(
            id=file_id,
        )

    # Create an empty file info in the database and get a file ID
    file_id = await db_manager.create_empty_file_info()

    # Add the file data to the message queue for further processing
    await __add_to_queue(file_bytes, filename, file_id)

    # Return a ShowFileID object with the file ID
    return ShowFileID(
        id=file_id,
    )


# Internal function to get S3 URLs by file ID
async def _get_urls_by_id(file_id: ShowFileID) -> ShowSplitURL:
    s3_urls = await db_manager.get_urls_by_id(file_id.id)
    return ShowSplitURL(
        s3_url_1=s3_urls[0],
        s3_url_2=s3_urls[1],
    )


# Define an API endpoint for uploading and splitting audio files
@split_router.post("/", response_model=ShowFileID)
async def split_audio(file: UploadFile) -> ShowFileID:
    return await _make_split(file)


# Define an API endpoint to get S3 URLs by file ID
@split_router.post("/show", response_model=ShowSplitURL)
async def get_s3_url(file_id: ShowFileID) -> ShowSplitURL:
    return await _get_urls_by_id(file_id)
