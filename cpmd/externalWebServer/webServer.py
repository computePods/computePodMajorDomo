from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

import asyncio
from hypercorn.config import Config
from hypercorn.asyncio import serve

#import webServer.publish

class NatsMsg(BaseModel):
  subject: str
  message: str

class SillyWebServer : 
  
  def __init__(self, aQueue, aNatsServer) :
    self.app = FastAPI()
    self.theQueue = aQueue
    self.theNatsServer = aNatsServer

    @self.app.get("/")
    async def read_root():
      return {"Hello": "World"}

    #self.addPublishInterface()
    
  async def runApp(self) :

    await self.theNatsServer.waitUntilRunning("testApp")
    
    config = Config()
    config.bind = ["0.0.0.0:8000"]
    await serve(self.app, config),

"""
Use os.getloadavg and os.cpu_count to get system information
"""
