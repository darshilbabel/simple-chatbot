from django.urls import path

from chatbot.views import ChatView, VoiceChatView

app_name = "chatbot"


urlpatterns = [
    path("chat/", ChatView.as_view(), name="chat"),
    path("voice-chat/", VoiceChatView.as_view(), name="voice-chat"),
]