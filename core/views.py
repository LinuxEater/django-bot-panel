from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.views.decorators.http import require_POST

from .models import BotTask, BotLog
from .forms import BotTaskForm
from .services import scrape_site, send_telegram


def dashboard(request):
    tasks = BotTask.objects.all()
    logs = BotLog.objects.select_related("task").all()[:20]
    return render(request, "core/dashboard.html", {"tasks": tasks, "logs": logs})


def task_create(request):
    if request.method == "POST":
        form = BotTaskForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Tarefa criada!")
            return redirect("dashboard")
    else:
        form = BotTaskForm()
    return render(request, "core/task_form.html", {"form": form, "title": "Nova tarefa"})


def task_edit(request, pk):
    task = get_object_or_404(BotTask, pk=pk)
    if request.method == "POST":
        form = BotTaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, "Tarefa atualizada!")
            return redirect("dashboard")
    else:
        form = BotTaskForm(instance=task)
    return render(request, "core/task_form.html", {"form": form, "title": "Editar tarefa"})


def task_toggle(request, pk):
    task = get_object_or_404(BotTask, pk=pk)
    task.active = not task.active
    task.save(update_fields=["active"])

    # Se ativou, envia imediatamente
    if task.active:
        text = scrape_site(task.url, task.css_selector or None)
        ok = send_telegram(task.token, task.chat_id, text)
        BotLog.objects.create(task=task, ran_at=timezone.now(), ok=ok, message=text)
        task.last_run = timezone.now()
        task.last_message = text
        task.save(update_fields=["last_run", "last_message"])
        messages.info(request, f"Tarefa ativada e mensagem enviada? {'✅' if ok else '❌'}")
    else:
        messages.info(request, "Tarefa desativada.")

    return redirect("dashboard")



def task_delete(request, pk):
    task = get_object_or_404(BotTask, pk=pk)
    task.delete()
    messages.warning(request, "Tarefa removida.")
    return redirect("dashboard")


def test_scrape(request, pk):
    task = get_object_or_404(BotTask, pk=pk)
    # Faz scraping
    text = scrape_site(task.url, task.css_selector or None)

    # Envia para o Telegram
    ok = send_telegram(task.token, task.chat_id, text)

    # Registra log
    BotLog.objects.create(task=task, ran_at=timezone.now(), ok=ok, message=text)

    # Atualiza última execução
    task.last_run = timezone.now()
    task.last_message = text
    task.save(update_fields=["last_run", "last_message"])

    # Mensagem no painel
    preview = text[:180] + ("…" if len(text) > 180 else "")
    messages.info(request, f"Mensagem enviada? {'✅' if ok else '❌'} - Preview: {preview}")

    return redirect("dashboard")



