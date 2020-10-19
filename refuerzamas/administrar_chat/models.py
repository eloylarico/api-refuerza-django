# Django
from django.db import models

# Model
from refuerzamas.clases.models import Chat


class ChatAdmin(Chat):
    class Meta:
        proxy = True
        verbose_name = "Administración chat"
        verbose_name_plural = "Administración chats"
