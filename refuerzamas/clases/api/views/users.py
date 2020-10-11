#Rest
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import mixins, viewsets
from django.contrib.auth import get_user_model

#Serialzier
from refuerzamas.clases.api.serializers import UserEstudianteModelSerializer, UserDocenteModelSerializer, UserTutorModelSerializer

#Model
from refuerzamas.clases.models import User



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



class DocenteViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):

    serializer_class = UserDocenteModelSerializer
    queryset = User.objects.all()

    def get_queryset(self):
        return self.queryset.filter(tipo_usuario = User.DOCENTE)