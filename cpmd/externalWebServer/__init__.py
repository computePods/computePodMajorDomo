from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

import asyncio
from hypercorn.config import Config
from hypercorn.asyncio import serve

import webServer.publish

class ExternalWebServer : 

  addPublishInterface = webServer.publish.addPublishInterface
  
  def __init__(self, aNatsClient, aNatsServer) :
    self.app = FastAPI()
    self.natsClient = aNatsClient
    self.natsServer = aNatsServer

    @self.app.get("/")
    async def read_root():
      return {"Hello": "World"}

    self.addPublishInterface()
    
  async def runApp(self) :

    await self.natsServer.waitUntilRunning("webServer")
    
    config = Config()
    config.bind = ["0.0.0.0:8000"]
    await serve(self.app, config),

"""
Use os.getloadavg and os.cpu_count to get system information
"""
