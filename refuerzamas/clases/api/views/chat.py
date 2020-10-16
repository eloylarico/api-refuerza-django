from django.http import Http404, JsonResponse
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from refuerzamas.clases.api.serializers import ChatModelSerializer, MensajeModelSerializer
from refuerzamas.clases.models import Chat, User, Mensaje


class ChatViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = ChatModelSerializer

    @action(detail=True, methods=["GET"])
    def mensajes(self, request, pk=None):
        user = self.request.user
        try:
            chat = user.get_chats().get(id=pk)
            mensajes = chat.mensajes.all()
            serializer = MensajeModelSerializer(mensajes, many=True)
            return JsonResponse(serializer.data, safe=False)
        except Chat.DoesNotExist:
            raise Http404

    @action(detail=True, methods=["POST"])
    def revisado(self, request, pk=None):
        user = self.request.user
        try:
            chat = user.get_chats().get(id=pk)
            chat.mensajes.exclude(user=user).filter(visto=False).update(visto=True)
            chats = user.get_chats()
            serializer = self.get_serializer(chats, many=True)
            return Response(serializer.data)
        except Chat.DoesNotExist:
            raise Http404

    def get_queryset(self):
        return self.request.user.get_chats()
