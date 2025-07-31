from django.views.generic import TemplateView


class ChatView(TemplateView):
    print("here")
    template_name = "chat/chat.html"

class VoiceChatView(TemplateView):
    template_name = "chat/voice_demo.html"


