from fastapi import FastAPI

from src.api.routers import split_router


# Create an instance of the FastAPI application
app = FastAPI(title="Audio Stereo Split Service")

# Include the router in the application with a prefix and tags
app.include_router(split_router, prefix="/split", tags=["split"])
