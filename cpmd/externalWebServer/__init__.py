from typing import Optional

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

import aiofiles
import asyncio
from hypercorn.config import Config
from hypercorn.asyncio import serve
import os

import interfaces.AllFastApiExamples
import interfaces.AllFastApiRoutes
import externalWebServer.publish

class ExternalWebServer :

  addPublishInterface = externalWebServer.publish.addPublishInterface

  def __init__(self, aNatsClient) :
    self.app = FastAPI()
    self.natsClient = aNatsClient

    interfaces.AllFastApiExamples.addAllExamples(self.app)
    interfaces.AllFastApiRoutes.addAllInterface(self.app)
    self.addPublishInterface()

    self.app.mount("/clientApp", StaticFiles(directory="clientApp"), name='clientApp')

    @self.app.get("/", response_class=HTMLResponse)
    async def read_root():
      print("externalWebServer cwd: {}".format(os.getcwd()))
      async with aiofiles.open('clientApp/mcv.html', mode='r') as f:
        mcvHtml = await f.read()
        return mcvHtml

  async def runApp(self, reload) :

// We will listen for NATS reload events (or changes to files in
// directories we are using) and then use the graceful shutdown to
// shutdown and restart the server.
//
// https://pgjones.gitlab.io/hypercorn/how_to_guides/api_usage.html#graceful-shutdown

    config = Config()
    config.bind = ["0.0.0.0:8000"]
    config.use_reload = reload
    config.accesslog  = '-'
    await serve(self.app, config),

"""
Use os.getloadavg and os.cpu_count to get system information
"""
