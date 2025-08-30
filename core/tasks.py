# core/tasks.py
from background_task import background
from .models import BotTask, BotLog
from .services import scrape_site, send_telegram
from django.utils import timezone

@background(schedule=0)
def run_scheduled_bots():
    now = timezone.localtime(timezone.now()).time()
    tasks = BotTask.objects.filter(active=True)
    for task in tasks:
        if task.schedule_time.hour == now.hour and task.schedule_time.minute == now.minute:
            text = scrape_site(task.url, task.css_selector or None)
            ok = send_telegram(task.token, task.chat_id, text)
            # Salva log
            BotLog.objects.create(task=task, ran_at=timezone.localtime(timezone.now()), ok=ok, message=text)
            task.last_run = timezone.localtime(timezone.now())
            task.last_message = text
            task.save(update_fields=["last_run", "last_message"])
