import json
from channels.generic.websocket import WebsocketConsumer

from asgiref.sync import async_to_sync

class ChatConsumer(WebsocketConsumer):
  def connect(self):
    self.strGroupName = 'chat'
    async_to_sync(self.channel_layer.group_add)(self.strGroupName, self.channel_name)

    # pprint.pprint(self.accept())
    self.accept()
  
  def disconnect(self, close_code):
    async_to_sync(self.channel_layer.group_discard)(self.strGroupName, self.channel_name)

  def receive(self, text_data):
    text_data_json = json.loads(text_data)

    strMessage = text_data_json['message']

    data = {
      'type': 'chat_message',
      'message': strMessage,
    }
    async_to_sync(self.channel_layer.group_send)(self.strGroupName, data)

  def chat_message(self, data):
    data_json = {
      'message': data['message'],
    }

    self.send(text_data=json.dumps(data_json))