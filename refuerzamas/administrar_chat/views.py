# Django
from django.http import JsonResponse
from django.contrib.auth.decorators import user_passes_test

# Models
from refuerzamas.clases.models import *

# Serializer
from refuerzamas.administrar_chat.serializers import *


@user_passes_test(lambda u: u.is_active and u.is_staff)
def list_docentes(request):
    docentes_chat = ChatUser.objects.filter(user__tipo_usuario=User.DOCENTE).distinct('user')
    data = []
    for d in docentes_chat:
        data.append({"id_user1": d.user.id, "name": d.user.display_name})
    return JsonResponse(data, safe=False)


@user_passes_test(lambda u: u.is_active and u.is_staff)
def list_chat_of_docente(request, id_docente):
    cc = Chat.objects.filter(chats_users__user__id=id_docente)
    lista = []
    for i in cc:
        uu = User.objects.filter(chats_users__chat=i).exclude(tipo_usuario=User.DOCENTE)
        dd = uu.first()
        lista.append(AdminUserModelSerializer(dd).data)
    return JsonResponse(lista, safe=False)


@user_passes_test(lambda u: u.is_active and u.is_staff)
def chat_all(request, user1, user2):
    c1 = Chat.objects.filter(chats_users__user__id=user1)
    c2 = Chat.objects.filter(chats_users__user__id=user2)
    chat = c1 & c2
    mensaje = chat[0].get_mensajes()
    serializer = AdminMensajeodelSerializer(mensaje, many=True)
    return JsonResponse(serializer.data, safe=False)
