# Rest
from django.http import Http404
from rest_framework import mixins, viewsets

# Serializer
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from django.core.exceptions import ValidationError as ModelValidationError
from rest_framework.response import Response

from refuerzamas.clases.api.serializers import ClaseModelSerializer

# Model
from refuerzamas.clases.models import Clase, User, Reserva


class ClasesUserViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = ClaseModelSerializer

    def get_queryset(self):
        if self.request.user.tipo_usuario == User.ESTUDIANTE:
            return Clase.clases.filter(estudiante=self.request.user.perfil_estudiante)

        elif self.request.user.tipo_usuario == User.DOCENTE:
            return Clase.clases.filter(docente=self.request.user.perfil_docente)

        elif self.request.user.tipo_usuario == User.TUTOR:
            return Clase.clases.filter(estudiante__tutor=self.request.user.perfil_tutor).distinct()


class ReservaViewSet(viewsets.GenericViewSet):
    serializer_class = ClaseModelSerializer
    queryset = Reserva.objects.all()

    @action(detail=True, methods=["POST"])
    def tomar(self, request, pk=None):
        try:
            user = self.request.user
            reserva = self.get_object()
            reserva.asignar(user.perfil_docente.id)
            serializer = self.get_serializer(reserva)
        except ModelValidationError:
            raise ValidationError("Esta clase ya ha sido tomada")
        return Response(serializer.data)
