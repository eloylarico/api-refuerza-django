# Rest
from rest_framework import serializers

# Model
from refuerzamas.clases.models import Clase

# Serializer
from refuerzamas.clases.api.serializers import UserEstudianteModelSerializer, UserDocenteModelSerializer


class ClaseUserModelSerializer(serializers.ModelSerializer):

    # docente = DocenteModelSerializer()
    docente = UserDocenteModelSerializer(source="get_docente__user", read_only=True)
    user = UserEstudianteModelSerializer(source="get_estudiante__user", read_only=True)
    # TODO Añadir curso

    class Meta:
        model = Clase
        fields = (
            "docente",
            "user",
            "precio_estudiante",
            "precio_docente",
            "medio_pago",
            "hora_inicio",
            "hora_fin",
            "estado",
            "motivo_reporte",
            "observaciones",
        )
