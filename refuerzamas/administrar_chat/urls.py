# Django
from django.urls import path

# Views
from refuerzamas.administrar_chat.views import *

urlpatterns = [
    path("list_users/", list_users, name="list_users"),
    path("list_chat/<int:id_user>/", list_chat_of_user, name="list_chats"),
    path("conversacion/<int:id_chat>/", get_conversacion, name="list_conversacion"),
]
