import os
import uvicorn
from backend.src import api_v1_router
from backend.src.create_app import create_app
# Create FastAPI app instance
app = create_app()


# Add routes
app.include_router(api_v1_router, prefix="/api")


# Launch FastAPI app
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)