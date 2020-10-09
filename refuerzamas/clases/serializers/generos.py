#Rest
from rest_framework import serializers

#Model
from refuerzamas.clases.models import Genero

class GenerosSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genero
        fields = ("nombre",)