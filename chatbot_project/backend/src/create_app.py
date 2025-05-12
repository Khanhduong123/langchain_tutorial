from fastapi import FastAPI
from backend.src.v1.config.swagger import swagger_config


# Define create_app function.
# Avoid circular import by using this function
# to create FastAPI app instance.
def create_app():
    app = FastAPI(**swagger_config)
    return app