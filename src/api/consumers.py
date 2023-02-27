from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json 

class ChatConsumer(WebsocketConsumer):
    room_name: str
    room_group_name: str

    _origins = ["scenario"]

    def connect(self):
        print("Connecting")
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        print(text_data_json)
        origin = text_data_json["origin"]
        if origin not in self._origins:
            return

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': origin,
                'message': text_data_json
            }
            
        )
    
    def scenario(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps(message))