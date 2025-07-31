import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'simple_chatbot.settings')

app = Celery('simple_chatbot', backend='redis://localhost', broker='redis://localhost')
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks([
    'chatbot.celery_tasks.common_chat_tasks',

])
