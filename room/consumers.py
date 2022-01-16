import json
import datetime

from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):

  def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)
      self.strGroupName = ''
      self.strUserName = ''

  async def connect(self):
    await self.accept()
  
  async def disconnect(self, close_code):
    await self.leave_chat()

  async def receive(self, text_data):
    text_data_json = json.loads(text_data)

    # 入室時処理
    if('join' == text_data_json.get('data_type')):
      self.strUserName = text_data_json["username"]
      await self.join_chat()
    # 退室時処理
    elif('leave' == text_data_json.get('data_type')):
      await self.leave_chat()
    # メッセージ受信時処理
    else:
      strMessage = text_data_json['message']

      data = {
        'type': 'chat_message',
        'message': strMessage,
        'username': self.strUserName,
        'datetime': datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S'),
      }
      await self.channel_layer.group_send(self.strGroupName, data)

  async def chat_message(self, data):
    data_json = {
      'message': data['message'],
      'username': data['username'],
      'datetime': data['datetime'],
    }
    
    await self.send(text_data=json.dumps(data_json))

  # 入室
  async def join_chat(self):
    self.strGroupName = 'chat'
    await self.channel_layer.group_add(self.strGroupName, self.channel_name)

  # 退室
  async def leave_chat(self):
    if('' == self.strGroupName):
      return
    
    await self.channel_layer.group_discard(self.strGroupName, self.channel_name)

    self.strGroupName = ''
