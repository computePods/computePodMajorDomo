from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

import asyncio
from hypercorn.config import Config
from hypercorn.asyncio import serve

import externalWebServer.publish

class ExternalWebServer : 

  addPublishInterface = externalWebServer.publish.addPublishInterface
  
  def __init__(self, aNatsClient) :
    self.app = FastAPI()
    self.natsClient = aNatsClient

    @self.app.get("/")
    async def read_root():
      return {"Hello": "World"}

    self.addPublishInterface()
    
  async def runApp(self) :

    config = Config()
    config.bind = ["0.0.0.0:8000"]
    await serve(self.app, config),

"""
Use os.getloadavg and os.cpu_count to get system information
"""
