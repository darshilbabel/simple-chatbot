import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from chatbot.models import ChatStatus
from chatbot.celery_tasks.chat_tasks import get_response, save_in_db


class ChatConsumer(WebsocketConsumer):

    def receive(self, text_data):
        session_id = 'daec8wia0ev2jxok9zv3duqkenoyrzjs'
        text_data_json = json.loads(text_data)
        print(text_data_json)
        async_to_sync(self.channel_layer.send)(
            self.channel_name,
            {
                "type": "chat_message",
                "text": {"msg": text_data_json["text"], "source": "user"},
            },
        )

        get_response.delay(self.channel_name, session_id, text_data_json)
        save_in_db.delay(session_id, 'User', text_data_json['text'], ChatStatus.IN_PROGRESS)

    def chat_message(self, event):
        text = event["text"]
        self.send(text_data=json.dumps({"text": text}))
