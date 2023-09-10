import asyncio

from pydub import AudioSegment

import aioboto3
from botocore.exceptions import ClientError

from src.settings import BUCKET_NAME


class S3Manager:
    def __init__(self, s3_client):
        self.s3_client = s3_client
        self.bucket_name = BUCKET_NAME

    async def create_bucket(self, region: str = 'us-east-1'):
        """
        Create an S3 bucket in a specified region asynchronously.

        If a region is not specified, the bucket is created in the S3 default region (us-east-1).

        :param bucket_name: The name of the bucket to create.
        :param region: The AWS region where the bucket should be created, e.g., 'us-west-2'.
        """
        try:
            buckets = await self._get_all_buckets()
            if self.bucket_name not in buckets:
                if region is None:
                    await self.s3_client.create_bucket(Bucket=self.bucket_name)
                else:
                    location = {'LocationConstraint': region}
                    await self.s3_client.create_bucket(
                        Bucket=self.bucket_name,
                        CreateBucketConfiguration=location
                    )
        except ClientError as e:
            print(f"Error: {e}")

    async def upload_audio(self, data: AudioSegment, file_hash: str, channel_number: int, extension: str):
        """
        Uploads an AudioSegment as a sound file to an Amazon S3 bucket

        :param data: The audio data to upload
        :param file_hash: A unique identifier or hash for the file
        :param channel_number: The channel number associated with the audio data
        :param extension: The file extension (e.g., 'mp3', 'wav') to use when saving the audio
        :return: The S3 URI of the uploaded sound file
        """
        try:
            filename = f'{file_hash}_{channel_number}.{extension}'
            audio_bytes = data.export(format=extension).read()

            # Upload bytes to S3 bucket
            await self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=f'{file_hash}_{channel_number}.{extension}',
                Body=audio_bytes
            )
            # Return s3 URI
            return f's3://{self.bucket_name}/{filename}'
        except Exception as e:
            print(f"Error uploading to S3: {e}")

    async def check_exist(self):
        ...

    async def _get_all_buckets(self) -> list[str]:
        """
        Get all local S3 buckets.
        """
        try:
            response = await self.s3_client.list_buckets()
            return [bucket['Name'] for bucket in response['Buckets']]
        except ClientError as e:
            print(f"Error: {e}")
