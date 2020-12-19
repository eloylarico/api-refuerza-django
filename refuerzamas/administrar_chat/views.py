# Django
from django.http import JsonResponse
from django.contrib.auth.decorators import user_passes_test

# Models
from refuerzamas.clases.models import *

# Serializer
from refuerzamas.administrar_chat.serializers import *


@user_passes_test(lambda u: u.is_active and u.is_staff)
def list_users(request):
    list_user = User.objects.all().exclude(chats_users__chat=None)
    serializer = AdminUserModelSerializer(list_user, many=True)
    return JsonResponse(serializer.data, safe=False)


@user_passes_test(lambda u: u.is_active and u.is_staff)
def list_chat_of_user(request, id_user):
    chats = Chat.objects.filter(chats_users__user__id=id_user)
    serializer = ChatModelSerializer(chats, many=True)
    return JsonResponse(serializer.data, safe=False)


@user_passes_test(lambda u: u.is_active and u.is_staff)
def get_conversacion(request, id_chat):
    chat = Chat.objects.get(id=id_chat)
    mensaje = chat.get_mensajes()
    serializer = AdminMensajeodelSerializer(mensaje, many=True)
    return JsonResponse(serializer.data, safe=False)
