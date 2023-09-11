import asyncio
import base64
import hashlib
import json

import aio_pika
import aioboto3

from aws import s3_manager
from initialize import db_manager, rabbitmq
from audio_processing import audio_splitter
import initialize


# Define a callback function to process incoming messages from the RabbitMQ queue
async def callback(message: aio_pika.IncomingMessage):
    # Parse the JSON data received in the message
    data = json.loads(message.body)

    # Decode and process the file data
    file_bytes = base64.b64decode(data['file_bytes'].encode('utf-8'))
    filename = data['filename']
    file_id = data['file_id']

    # Split the audio into channels
    audio_channels = await audio_splitter.split_audio(file_bytes)

    # Calculate the hash and extension of the file
    file_hash = hashlib.sha256(file_bytes).hexdigest()
    extension = filename.split('.')[-1]

    # Upload audio channels to an S3 bucket using aioboto3 and obtain S3 URLs
    async with aioboto3.Session().client('s3') as s3_client:
        bucket_manager = s3_manager.S3Manager(s3_client)
        await bucket_manager.create_bucket()
        s3_urls = []
        for channel_number, channel in enumerate(audio_channels):
            s3_urls.append(await bucket_manager.upload_audio(channel, file_hash, channel_number, extension))

    # Update the database with file information and request history
    await db_manager.update_file_info(file_id, s3_urls[0], s3_urls[1])
    await db_manager.add_request_info(file_hash, file_id)

    # Acknowledge and remove the processed message from the queue
    await message.ack()


# Define the main asynchronous function to run the RabbitMQ consumer
async def main():
    # Initialize required resources
    await initialize.init()

    # Start consuming messages from the RabbitMQ queue using the defined callback
    await rabbitmq.queue.consume(callback)

    try:
        # Wait until termination (program continues running)
        await asyncio.Future()
    finally:
        # Close resources gracefully upon termination
        await initialize.close()


if __name__ == "__main__":
    asyncio.run(main())
