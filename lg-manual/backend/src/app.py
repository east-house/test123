import os 
from logging import getLogger

from fastapi import FastAPI
from routes import routers
# from configuration import APIConfigurations

app = FastAPI(
    # title=APIConfigurations.title,
    # description=APIConfigurations.description,
    # version=APIConfigurations.version,
)

app.include_router(routers.router, prefix="", tags=[""])