# Django
from django.urls import path

# Views
from refuerzamas.administrar_chat.views import (
    list_chat_of_docente,
    list_docentes,
    chat_all,
)

urlpatterns = [
    path("list_docentes/", list_docentes, name="list_docentes"),
    path("list_chat/<int:id_docente>/", list_chat_of_docente, name="list_chats"),
    path("all_chat/<int:user1>/<int:user2>/", chat_all, name="all_chat"),
]
