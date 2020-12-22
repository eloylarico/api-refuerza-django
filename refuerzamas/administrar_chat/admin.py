# # Django
from django.contrib import admin
#
# # models
from .models import ChatAdmin


@admin.register(ChatAdmin)
class ChatAdmin(admin.ModelAdmin):
    change_list_template = "metricas/chat_metricas.html"

    def has_add_permission(self, request, obj=None) -> bool:
        return False