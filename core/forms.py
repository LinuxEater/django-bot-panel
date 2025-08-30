from django import forms
from .models import BotTask

class BotTaskForm(forms.ModelForm):
    class Meta:
        model = BotTask
        fields = [
            "name",
            "url",
            "css_selector",
            "token",
            "chat_id",
            "schedule_time",
            "active"
        ]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Nome do bot"}),
            "url": forms.URLInput(attrs={"placeholder": "URL do site"}),
            "css_selector": forms.TextInput(attrs={"placeholder": "Seletor CSS (opcional)"}),
            "token": forms.TextInput(attrs={"placeholder": "Token do Telegram"}),
            "chat_id": forms.TextInput(attrs={"placeholder": "Chat ID"}),
            "schedule_time": forms.TimeInput(
                format="%H:%M",
                attrs={"type": "time", "placeholder": "HH:MM"}
            ),
            "active": forms.CheckboxInput(),
        }
        error_messages = {
            'name': {'required': 'O nome do bot é obrigatório.'},
            'url': {'required': 'A URL é obrigatória.', 'invalid': 'Digite uma URL válida.'},
            'token': {'required': 'O token do Telegram é obrigatório.'},
            'chat_id': {'required': 'O Chat ID é obrigatório.'},
            'schedule_time': {'required': 'O horário é obrigatório.', 'invalid': 'Digite um horário válido (HH:MM).'},
        }