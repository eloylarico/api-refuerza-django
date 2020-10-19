# Rest
from rest_framework import serializers

# Model
from refuerzamas.clases.models import User, Chat, Mensaje, Docente


class AdminUserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "display_name", "tipo_usuario", "avatar"]


class AdminChatModelSerializer(serializers.ModelSerializer):

    user2 = AdminUserModelSerializer(read_only=True)

    class Meta:
        model = Chat
        fields = ["user2"]


class AdminMensajeodelSerializer(serializers.ModelSerializer):

    user = AdminUserModelSerializer(read_only=True)

    class Meta:
        model = Mensaje
        fields = ["user", "texto", "archivo", "date_formatting", "visto"]


class AdminChatMensajeModelSerializer(serializers.ModelSerializer):

    mensajes = AdminMensajeodelSerializer(read_only=True, many=True)

    class Meta:
        model = Chat
        fields = ["mensajes"]
