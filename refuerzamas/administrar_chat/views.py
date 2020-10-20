# Django
from django.http import JsonResponse
from django.contrib.auth.decorators import user_passes_test

# Models
from refuerzamas.clases.models import Chat, Docente, User

# Serializer
from refuerzamas.administrar_chat.serializers import AdminChatModelSerializer, AdminChatMensajeModelSerializer


@user_passes_test(lambda u: u.is_active and u.is_staff)
def list_docentes(request):
    docente = Docente.objects.all()
    data = []
    for d in docente:
        data.append({"id_user1": d.user.id, "name": d.user.display_name})
    return JsonResponse(data, safe=False)


@user_passes_test(lambda u: u.is_active and u.is_staff)
def list_chat_of_docente(request, id_docente):
    chat = Chat.objects.filter(user1__id=id_docente, activo=True).exclude(mensajes=None)
    serializer = AdminChatModelSerializer(chat, many=True)
    return JsonResponse(serializer.data, safe=False)


@user_passes_test(lambda u: u.is_active and u.is_staff)
def chat_all(request, user1, user2):
    user1 = User.objects.get(id=user1)
    user2 = User.objects.get(id=user2)
    chat = Chat.objects.get(user1=user1, user2=user2)
    serializer = AdminChatMensajeModelSerializer(chat)
    return JsonResponse(serializer.data)