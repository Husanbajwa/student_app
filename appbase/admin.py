from django.contrib import admin

# Register your models here.
from .models import Message, Room, Topic , User
from .models import Thread, ChatMessage

admin.site.register(ChatMessage)


class ChatMessage(admin.TabularInline):
    model = ChatMessage

admin.site.register(User)
admin.site.register(Room)
admin.site.register(Topic)
admin.site.register(Message)

class ThreadAdmin(admin.ModelAdmin):
    inlines = [ChatMessage]
    class Meta:
        model = Thread


admin.site.register(Thread, ThreadAdmin)