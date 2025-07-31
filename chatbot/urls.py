from django.urls import path

from chatbot.views import ChatView

app_name = "chatbot"


urlpatterns = [
    path("chat/", ChatView.as_view(), name="chat"),
]