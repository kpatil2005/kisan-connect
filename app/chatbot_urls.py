from django.urls import path
from . import chatbot_standalone

# Standalone chatbot URLs
chatbot_urlpatterns = [
    path('ai-chat/', chatbot_standalone.ai_chatbot, name='ai_chatbot'),
]