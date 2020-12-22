# Rest
from django.db.models import fields
from rest_framework import serializers

# Model
from refuerzamas.clases.models import *


class AdminUserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "display_name", "tipo_usuario", "number_type",  "avatar"]


class ChatModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ["id", "titulo", "imagen", "activo", "get_participantes"]


class ChatUserModelSerializer(serializers.ModelSerializer):
    user = AdminUserModelSerializer(read_only=True)
    class Meta:
        model = ChatUser
        fields = ["user"]

class AdminMensajeodelSerializer(serializers.ModelSerializer):

    chat_user = ChatUserModelSerializer(read_only=True)

    class Meta:
        model = Mensaje
        fields = ["chat_user", "texto", "archivo", "date_formatting"]

