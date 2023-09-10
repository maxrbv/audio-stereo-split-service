from pydantic import BaseModel
from fastapi import UploadFile, File


# API models
class ShowSplit(BaseModel):
    id: int
    s3_url_1: str
    s3_url_2: str


class AudioFile(BaseModel):
    audio_file: UploadFile
