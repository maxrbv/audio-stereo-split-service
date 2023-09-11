from pydantic import BaseModel


# API models
class ShowFileID(BaseModel):
    """
    Pydantic model representing the response structure for returning a file ID
    """
    id: int


class ShowSplitURL(BaseModel):
    """
    Pydantic model representing the response structure for returning S3 URLs of split audio files
    """
    s3_url_1: str
    s3_url_2: str
