from django.contrib.auth import get_user_model
from rest_framework import parsers, renderers
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.exceptions import PermissionDenied
from rest_framework.views import APIView
from rest_framework.compat import coreapi, coreschema

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from refuerzamas.clases.models import User


class ObtainDocenteAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        if user.tipo_usuario != User.DOCENTE:
            raise PermissionDenied
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key})


obtain_docente_token = ObtainDocenteAuthToken.as_view()


class ObtainEstudianteTutorAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        if user.tipo_usuario != User.ESTUDIANTE and user.tipo_usuario != user.TUTOR:
            raise PermissionDenied
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key})


obtain_estudiante_tutor_token = ObtainEstudianteTutorAuthToken.as_view()
