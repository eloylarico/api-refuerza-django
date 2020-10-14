# Rest
from rest_framework import mixins, viewsets

# Serializer
from refuerzamas.clases.api.serializers import ClaseModelSerializer

# Model
from refuerzamas.clases.models import Clase, User


class ClasesUserViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):

    serializer_class = ClaseModelSerializer

    def get_queryset(self):
        if self.request.user.tipo_usuario == User.ESTUDIANTE:
            return Clase.clases.filter(estudiante=self.request.user.perfil_estudiante)

        elif self.request.user.tipo_usuario == User.DOCENTE:
            return Clase.clases.filter(docente=self.request.user.perfil_docente)

        elif self.request.user.tipo_usuario == User.TUTOR:
            return Clase.clases.filter(estudiante__tutor=self.request.user.perfil_tutor)
