from typing import Optional, List
from fastapi import FastAPI
from pydantic import BaseModel

# WebServer interface definition....

class NatsMsg(BaseModel):
  subject: str
  message: List

def addPublishInterface(self) :
  @self.app.put("/publish")
  async def update_item(msg: NatsMsg):
    await self.natsClient.sendMessage(msg)
    return { "done": True }


