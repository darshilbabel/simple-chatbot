import os

from asgiref.sync import async_to_sync
from celery import shared_task
from channels.layers import get_channel_layer
from django.contrib.sessions.models import Session
from openai import OpenAI

from chatbot.models import LLMModel, Profile
from chatbot.models import Chat, ChatStatus

channel_layer = get_channel_layer()
client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

@shared_task
def get_response(channel_name, session_id, input_data):
    chats = Chat.objects.filter(session=session_id)
    if len(chats) > 0:
        chats = chats.order_by('created_at')
    messages = []
    ai_user = Profile.objects.get(id=1)
    messages.append({
        'role': 'system',
        'content': input_data['context']
    })
    for chat in chats:
        if chat.receiver == ai_user:
            messages.append({
                'role': 'user',
                'content': chat.message
            })
        else:
            messages.append({
                'role': 'assistant',
                "content": chat.message
            })
    messages.append({
        'role': 'user',
        'content': input_data['text']
    })

    response = client.chat.completions.create(
        model=LLMModel.GPT4_O_MINI,
        messages=messages,
        stream=True
    )

    completion_text = ''
    for event in response:
        event_text = event.choices[0].delta
        finish_reason = event.choices[0].finish_reason
        if event_text.content is not None:
            completion_text += event_text.content
            async_to_sync(channel_layer.send)(
                channel_name,
                {
                    "type": "chat.message",
                    "text": {"msg": event_text.content, "source": "bot", "finish_reason": finish_reason},
                },
            )
        else:
            async_to_sync(channel_layer.send)(
                channel_name,
                {
                    "type": "chat.message",
                    "text": {"msg": "", "source": "bot", "finish_reason": finish_reason},
                },
            )
    if len(chats) == 1:
        save_in_db(session_id, 'AI', input_data['context'], ChatStatus.IN_PROGRESS)
    save_in_db(session_id, 'AI', completion_text, ChatStatus.IN_PROGRESS)
    return completion_text


@shared_task
def save_in_db(session_id, initiated_by, message, status):
    uid = 2
    if initiated_by == 'AI':
        receiver = Profile.objects.get(id=uid)
        sender = Profile.objects.get(id=1)
    else:
        sender = Profile.objects.get(id=uid)
        receiver = Profile.objects.get(id=1)
    chat = Chat(
        message=message,
        sender=sender,
        receiver=receiver,
        session=session_id,
        status=status
    )
    chat.save()
