# Rest
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import RetrieveUpdateAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework import mixins, viewsets, status
from django.contrib.auth import get_user_model

# Serialzier
from rest_framework.response import Response

from refuerzamas.clases.api.serializers import (
    UserEstudianteModelSerializer,
    UserDocenteModelSerializer,
    UserTutorModelSerializer,
    HoraModelSerializer,
    DiaModelSerializer,
)

# Model
from refuerzamas.clases.models import Estudiante, User, Clase, Docente, Dia


class UserDetailView(RetrieveUpdateAPIView):
    def get_object(self):
        return self.request.user

    def get_queryset(self):
        return get_user_model().objects.none()

    def get_serializer_class(self):
        if self.request.user.tipo_usuario == User.ESTUDIANTE:
            return UserEstudianteModelSerializer
        elif self.request.user.tipo_usuario == User.DOCENTE:
            return UserDocenteModelSerializer
        elif self.request.user.tipo_usuario == User.TUTOR:
            return UserTutorModelSerializer


class DocenteViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):

    serializer_class = UserDocenteModelSerializer

    def get_queryset(self):
        user = self.request.user
        # Si es docente o admin, no tiene autorizacion
        if user.tipo_usuario == User.DOCENTE or user.tipo_usuario is None:
            raise PermissionDenied
        # Si es estudiante, que  muestre solo los profes de su nivel
        elif user.tipo_usuario == User.ESTUDIANTE:
            # Si el usuario no ha definido su nivel, tiene acceso a todos
            if user.perfil_estudiante.grado is None:
                queryset = User.objects.filter(tipo_usuario=User.DOCENTE)
            else:
                nivel_usuario = user.perfil_estudiante.grado.nivel.id
                # Se hace este queryset para posteriormente ordenarlo aleatoriamente sin el problema de los ids repetidos
                # https://docs.djangoproject.com/en/3.0/ref/models/querysets/#distinct
                ids_user_docentes = User.objects.filter(
                    perfil_docente__cursos__grado__nivel_id=nivel_usuario
                ).values_list("id", flat=True)
                queryset = User.objects.filter(id__in=ids_user_docentes)

        # Si es tutor, que  muestre solo los profes del nivel de sus tutelados
        else:
            niveles_tutelados = (
                Estudiante.objects.filter(tutor__user_id=user.id, grado__isnull=False)
                .distinct()
                .values_list("grado__nivel_id", flat=True)
            )
            # Si sus tutelados no ha definido su nivel, tiene acceso a todos
            if len(niveles_tutelados) == 0:
                queryset = User.objects.filter(tipo_usuario=User.DOCENTE)
            else:
                ids_user_docentes = (
                    User.objects.filter(
                        perfil_docente__cursos__grado__nivel_id__in=niveles_tutelados
                    )
                    .distinct()
                    .values_list("id", flat=True)
                )
                # Se hace este queryset para posteriormente ordenarlo aleatoriamente sin el problema de los ids repetidos
                # https://docs.djangoproject.com/en/3.0/ref/models/querysets/#distinct
                queryset = User.objects.filter(id__in=ids_user_docentes)

        # Puedes acceder a todos los docentes de tu nivel, pero se te pueden listar máximo 5
        if self.action == "list":
            queryset = queryset.order_by("?")[:5]
        return queryset

    @action(detail=False, methods=["GET"])
    def mis_docentes(self, request):
        user = self.request.user
        if user.tipo_usuario == User.ESTUDIANTE or user.tipo_usuario == User.TUTOR:
            mis_docentes = user.get_mis_docentes()
            serializer = UserDocenteModelSerializer(
                mis_docentes, many=True, context={"request": request}
            )
            return Response(serializer.data)
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=["POST"])
    def guardar_horario_disponible(self, request):
        user = self.request.user
        if user.tipo_usuario == User.DOCENTE:
            horario = request.data.get("horario")
            user.perfil_docente.set_horario(horario)
            serializer = UserDocenteModelSerializer(user, context={"request": request})
            return Response(serializer.data)
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class EstudianteViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    serializer_class = UserEstudianteModelSerializer
    queryset = User.objects.filter(tipo_usuario=User.ESTUDIANTE).order_by("?")[:5]
