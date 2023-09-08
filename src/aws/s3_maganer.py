import asyncio

import aioboto3
from botocore.exceptions import ClientError


class S3Manager:
    def __init__(self, s3_client):
        self.s3_client = s3_client

    async def create_bucket(self, bucket_name: str, region: str = None):
        """
        Create an S3 bucket in a specified region asynchronously.

        If a region is not specified, the bucket is created in the S3 default region (us-east-1).

        :param bucket_name: The name of the bucket to create.
        :param region: The AWS region where the bucket should be created, e.g., 'us-west-2'.
        """
        try:
            buckets = await self._get_all_buckets()
            if bucket_name not in buckets:
                if region is None:
                    await self.s3_client.create_bucket(Bucket=bucket_name)
                else:
                    location = {'LocationConstraint': region}
                    await self.s3_client.create_bucket(
                        Bucket=bucket_name,
                        CreateBucketConfiguration=location
                    )
        except ClientError as e:
            print(f"Error: {e}")

    async def _get_all_buckets(self) -> list[str]:
        """
        Get all S3 buckets.
        """
        try:
            response = await self.s3_client.list_buckets()
            return [bucket['Name'] for bucket in response['Buckets']]
        except ClientError as e:
            print(f"Error: {e}")

    async def upload(self):
        ...

    async def check_exist(self):
        ...


async def test():
    async with aioboto3.Session().client('s3') as s3_client:
        bucket_manager = S3Manager(s3_client)
        bucket_name = "maxrbv-test"
        region = "us-west-2"

        await bucket_manager.create_bucket(bucket_name, region)


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(test())
