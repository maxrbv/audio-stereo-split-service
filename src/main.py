import uvicorn

from fastapi import FastAPI

from api.routes import split_router
import initialize as initialize

# Create an instance of the FastAPI application
app = FastAPI(title="Audio Stereo Split Service")

# Include the router in the application with a prefix and tags
app.include_router(split_router, prefix="/split", tags=["split"])


# Define an event handler to run on application startup
@app.on_event('startup')
async def init():
    """
    Event handler for application startup
    This function initializes resources or connections needed by the application
    """
    await initialize.init()  # Initialize resources


# Define an event handler to run on application shutdown
@app.on_event('shutdown')
async def close():
    """
    Event handler for application shutdown
    This function closes resources or connections gracefully when the application exits
    """
    await initialize.close()  # Close resources gracefully


# Start the FastAPI application using Uvicorn when the script is executed directly
if __name__ == '__main__':
    uvicorn.run(app)
