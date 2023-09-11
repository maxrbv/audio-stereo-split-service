import base64
import json

import aio_pika

from settings import RABBITMQ_QUEUE_NAME


class RabbitMQ:
    def __init__(self, rabbitmq_url: str):
        self.rabbitmq_url = rabbitmq_url
        self.connection = None
        self.channel = None
        self.queue = None
        self.queue_name = RABBITMQ_QUEUE_NAME

    async def init(self):
        # Initialize the RabbitMQ connection, channel, and queue
        self.connection = await aio_pika.connect(self.rabbitmq_url)
        self.channel = await self.connection.channel()
        self.queue = await self.channel.declare_queue(self.queue_name)

    async def close(self):
        # Close the RabbitMQ connection
        await self.connection.close()

    async def publish(self, file_bytes: bytes, filename: str, file_id: int):
        # Convert the binary data to a Base64-encoded string
        file_bytes_base64 = base64.b64encode(file_bytes).decode('utf-8')

        # Create a dictionary or data structure with the parameters
        message_data = {
            'file_bytes': file_bytes_base64,
            'filename': filename,
            'file_id': file_id
        }

        # Serialize the dictionary to JSON
        message_body = json.dumps(message_data)

        # Publish the JSON message to the RabbitMQ queue
        await self.channel.default_exchange.publish(
            aio_pika.Message(body=message_body.encode('utf-8')),
            routing_key=self.queue_name  # Specify the routing key (queue name)
        )
