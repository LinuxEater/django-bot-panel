from .models import BotTask
from .services import scrape_site, send_telegram
from django.utils import timezone

def run_scheduled_bots():
    now = timezone.localtime(timezone.now()).time()
    tasks = BotTask.objects.filter(active=True)
    for task in tasks:
        if task.schedule_time.hour == now.hour and task.schedule_time.minute == now.minute:
            text = scrape_site(task.url, task.css_selector or None)
            ok = send_telegram(task.token, task.chat_id, text)
            task.last_run = timezone.localtime(timezone.now())
            task.last_message = text
            task.save(update_fields=["last_run", "last_message"])
