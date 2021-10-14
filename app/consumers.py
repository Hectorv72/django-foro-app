from channels.consumer import AsyncConsumer
import asyncio
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from asgiref.sync import async_to_sync


from .models import *
#serializador json
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
import json
#AsyncJsonWebsocketConsumer

#while 1:
#await self.send({
        #    "type": "websocket.send",
        #    "text": event["text"]
        #})
        #print(event)
        #await asyncio.sleep(1)
        #await self.send_json("s")

class RealTime(AsyncJsonWebsocketConsumer):


    async def connect(self):
        await self.accept()

        #while 1:
        #    await asyncio.sleep(5)
        #    await self.send_json("s")

    
    async def websocket_receive(self,event):
        lel = serializers.serialize('json',Foros.objects.all())

        while 1:
            await asyncio.sleep(5)
            await self.send_json( lel )
            

class EchoConsumer(AsyncConsumer):
    async def websocket_connect(self,event):
        await self.send({
            "type": "websocket.accept"
        })

    async def websocket_receive(self,event):
        await self.send({
            "type": "websocket.send",
            "text": event["text"]
        })