from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

import asyncio
from hypercorn.config import Config
from hypercorn.asyncio import serve

#import webServer.publish

class PodWebServer :

  def __init__(self, aNatsClient) :
    self.app = FastAPI()
    self.natsClient = aNatsClient

    @self.app.get("/")
    async def read_root():
      return {"Hello": "World"}

#    self.addPublishInterface()

  async def runApp(self, reload) :

    config = Config()
    config.bind = ["127.0.0.1:8080"]
    config.use_reload = reload
    await serve(self.app, config),

"""
Use os.getloadavg and os.cpu_count to get system information
"""
