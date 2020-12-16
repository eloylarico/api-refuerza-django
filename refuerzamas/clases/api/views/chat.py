from django.http import Http404, JsonResponse
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from url_filter.integrations.drf import DjangoFilterBackend

from refuerzamas.clases.api.paginations import MensajesPagination
from refuerzamas.clases.api.serializers import ChatModelSerializer, MensajeModelSerializer
from refuerzamas.clases.models import Chat, ChatUser


class ChatViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = ChatModelSerializer

    def get_queryset(self):
        return self.request.user.get_chats().filter(activo=True)

    @action(detail=True, methods=["GET"])
    def mensajes(self, request, pk=None):
        user = self.request.user
        chat = get_object_or_404(Chat, pk=pk)

        # chat = user.get_chats().get(id=pk)
        mensajes = chat.get_mensajes()
        paginator = MensajesPagination()
        page = paginator.paginate_queryset(queryset=mensajes, request=request)
        if page is not None:
            serializer = MensajeModelSerializer(page, many=True, context=self.get_serializer_context())
            return paginator.get_paginated_response(serializer.data)
        serializer = MensajeModelSerializer(mensajes, many=True, context=self.get_serializer_context())
        return Response(serializer.data)

    # @action(detail=True, methods=["POST"])
    # def revisado(self, request, pk=None):
    #     user = self.request.user
    #     try:
    #         chat = user.get_chats().get(id=pk)
    #         chat.mensajes.exclude(user=user).filter(visto=False).update(visto=True)
    #         chats = user.get_chats()
    #         serializer = self.get_serializer(chats, many=True)
    #         return Response(serializer.data)
    #     except Chat.DoesNotExist:
    #         raise Http404


class MensajeViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = MensajeModelSerializer
    pagination_class = MensajesPagination
    filter_backends = [DjangoFilterBackend]
    filter_fields = ["chat_user"]

    # def create(self, request, *args, **kwargs):
    #     data = request.data
    #     data["user"] = self.request.user.id
    #     serializer = self.get_serializer(data=data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data)

    # def create(self, request, *args, **kwargs):
    #     data = request.data
    #     user_id = self.request.user.id
    #     chat_id = data['chat_id']
    #     chat_user = ChatUser.objects.get(user_id=user_id, chat_id=chat_id)
    #     data["user"] = user_id
    #     data["chat_user_id"] = chat_user.id
    #     del data['chat_id']
    #     serializer = self.get_serializer(data=data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data)
