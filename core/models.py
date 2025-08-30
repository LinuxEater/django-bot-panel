from django.db import models
from django.utils import timezone


class BotTask(models.Model):
    name = models.CharField("Nome", max_length=100)
    url = models.URLField("URL para scraping")
    css_selector = models.CharField(
    "CSS Selector (opcional)", max_length=255, blank=True,
    help_text="Ex.: h1.title ou .price .value. Se vazio, envia o <title> da página"
    )


    token = models.CharField("Token do Bot Telegram", max_length=200)
    chat_id = models.CharField("Chat ID do Telegram", max_length=50)


    schedule_time = models.TimeField(
    "Horário diário (HH:MM)", help_text="Horário local (America/Sao_Paulo)"
    )
    active = models.BooleanField("Ativo?", default=True)


    last_run = models.DateTimeField("Última execução", null=True, blank=True)
    last_message = models.TextField("Última mensagem enviada", blank=True)


    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ["-updated_at"]
        verbose_name = "Tarefa"
        verbose_name_plural = "Tarefas"


    def __str__(self):
        return f"{self.name} @ {self.schedule_time}"


class BotLog(models.Model):
    task = models.ForeignKey(BotTask, on_delete=models.CASCADE, related_name="logs")
    ran_at = models.DateTimeField(default=timezone.now)
    ok = models.BooleanField(default=False)
    message = models.TextField(blank=True)


    class Meta:
        ordering = ["-ran_at"]
        verbose_name = "Log"
        verbose_name_plural = "Logs"


    def __str__(self):
        status = "OK" if self.ok else "ERRO"
        return f"[{status}] {self.task.name} @ {self.ran_at:%Y-%m-%d %H:%M}"