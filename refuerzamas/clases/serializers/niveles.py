#Rest
from rest_framework import serializers

#Model
from refuerzamas.clases.models import Nivel, Grado

class NivelesModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Nivel
        fields = ("nombre", "descripcion", "orden","foto")


class GradoModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Grado
        fields = ("nombre", "descripcion", "orden")