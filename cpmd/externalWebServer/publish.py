from typing import Optional
from fastapi import FastAPI
from natsClient import NatsMsg

# WebServer interface definition....

def addPublishInterface(self) :
  @self.app.put("/publish")
  async def update_item(msg: NatsMsg):
    await self.natsClient.sendMessage(msg)
    return { "done": True }


