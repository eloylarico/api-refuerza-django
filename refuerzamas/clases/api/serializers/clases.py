#Rest
from rest_framework import serializers

#Model
from refuerzamas.clases.models import Clase

#Serializer
from refuerzamas.clases.api.serializers import DocenteModelSerializer

class ClaseUserModelSerializer(serializers.ModelSerializer):

    docente = DocenteModelSerializer()

    class Meta:
        model = Clase
        fields = ("docente","precio_estudiante","precio_docente","medio_pago","hora_inicio","hora_fin", "estado", "motivo_reporte","observaciones")