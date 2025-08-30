from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import BotTask, BotLog


@admin.register(BotTask)
class BotTaskAdmin(admin.ModelAdmin):
    list_display = ("name", "url", "schedule_time", "active", "last_run")
    search_fields = ("name", "url", "chat_id")
    list_filter = ("active",)


@admin.register(BotLog)
class BotLogAdmin(admin.ModelAdmin):
    list_display = ("task", "ran_at", "ok")
    list_filter = ("ok", "ran_at")
    search_fields = ("task__name", "message")