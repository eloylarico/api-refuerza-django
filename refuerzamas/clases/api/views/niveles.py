# Rest
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response

# Serialzier
from refuerzamas.clases.api.serializers import (
    NivelModelSerializer,
    GradoModelSerializer,
)

# Model
from refuerzamas.clases.models import Nivel, Grado


class NivelesGradoView(viewsets.ReadOnlyModelViewSet):

    serializer_class = NivelModelSerializer
    queryset = Nivel.objects.all()
    permission_classes = [AllowAny]

    @action(detail=True, methods=["get"])
    def grados(self, request, *args, **kwargs):
        nivel = self.get_object()
        queryset = Grado.objects.filter(nivel=nivel)
        serializer = GradoModelSerializer(queryset, many=True)
        return Response(serializer.data)
