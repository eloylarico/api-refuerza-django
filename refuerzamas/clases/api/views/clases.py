#Rest
from rest_framework import mixins, viewsets

#Serializer
from refuerzamas.clases.serializers import ClaseUserModelSerializer

#Model
from refuerzamas.clases.models import Clase, User


class ClasesUserViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):

    serializer_class = ClaseUserModelSerializer
    queryset = Clase.objects.all()

    def get_queryset(self):
        if self.request.user.tipo_usuario == User.ESTUDIANTE:
            return self.queryset.filter(estudiante = self.request.user.perfil_estudiante)

        elif self.request.user.tipo_usuario == User.DOCENTE:
            return self.queryset.filter(docente = self.request.user.perfil_docente)
        
        elif self.request.user.tipo_usuario == User.TUTOR:
            return self.queryset.filter(estudiante__tutor = self.request.user.perfil_tutor)