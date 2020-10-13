from django.http import Http404, JsonResponse
from rest_framework import mixins, viewsets
from rest_framework.decorators import action

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


    def get_queryset(self):
        return self.request.user.get_chats()


