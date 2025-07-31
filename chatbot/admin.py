from django.contrib import admin
from .models import Bot, Profile, Chat

@admin.register(Bot)
class BotAdmin(admin.ModelAdmin):
    list_display = ['name', 'provider', 'llm_model', 'created_at']
    search_fields = ['name', 'provider']

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'email', 'phone', 'profile_type']
    search_fields = ['email', 'phone']

@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ['session', 'sender', 'receiver', 'created_at', 'status']
    search_fields = ['session']
    list_filter = ['status', 'created_at']
