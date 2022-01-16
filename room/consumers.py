import json

from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
  async def connect(self):
    self.strGroupName = 'chat'
    await self.channel_layer.group_add(self.strGroupName, self.channel_name)

    await self.accept()
  
  async def disconnect(self, close_code):
    await self.channel_layer.group_discard(self.strGroupName, self.channel_name)

  async def receive(self, text_data):
    text_data_json = json.loads(text_data)

    strMessage = text_data_json['message']

    data = {
      'type': 'chat_message',
      'message': strMessage,
    }
    await self.channel_layer.group_send(self.strGroupName, data)

  async def chat_message(self, data):
    data_json = {
      'message': data['message'],
    }

    await self.send(text_data=json.dumps(data_json))