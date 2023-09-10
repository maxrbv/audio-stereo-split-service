from database.db_manager import DBManager
from rabbitmq_service.rabbitmq import RabbitMQ
from settings import RABBITMQ_URL, DATABASE_URL


# Create instances of the DBManager and RabbitMQ classes
db_manager = DBManager(DATABASE_URL)
rabbitmq = RabbitMQ(RABBITMQ_URL)


# Define an initialization function for the application
async def init():
    """
    Initialize the application by initializing the database manager and RabbitMQ connection
    """
    await db_manager.init()  # Initialize the database connection
    await rabbitmq.init()    # Initialize the RabbitMQ connection


# Define a function to close resources when the application exits
async def close():
    """
    Close resources, including the database connection and RabbitMQ connection, when the application exits
    """
    await db_manager.close()  # Close the database connection
    await rabbitmq.close()    # Close the RabbitMQ connection
