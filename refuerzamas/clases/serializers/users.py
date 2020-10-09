#Rest
from rest_framework import serializers

#User
from refuerzamas.clases.models import User

#Serializer
from refuerzamas.clases.serializers import GenerosSerializer

class UserModelSerializer(serializers.ModelSerializer):
    
    genero = GenerosSerializer()

    class Meta:
        model = User
        fields = ("username","nickname", "tipo_usuario", "avatar", "fecha_nacimiento", "genero", "celular", "email", "direccion", "observaciones")