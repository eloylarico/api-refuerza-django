from abc import ABC

from rest_framework.authentication import BaseAuthentication, get_authorization_header
from rest_framework import exceptions

from refuerzamas.clases.models import Docente, Estudiante


class RefuerzamasBaseAuthentication(BaseAuthentication):
    keyword = "Token"
    model = None

    def authenticate(self, request):
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != self.keyword.lower().encode():
            return None

        if len(auth) == 1:
            msg = "Header invalido, no se ha proveído el token."
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = "Header del token invalido, el token no debe tener espacios en blanco."
            raise exceptions.AuthenticationFailed(msg)

        try:
            token = auth[1].decode()
        except UnicodeError:
            msg = "Header del token invalido, el token contiene carácteres inválidos."

            raise exceptions.AuthenticationFailed(msg)

        return self.authenticate_credentials(token)

    def authenticate_credentials(self, token):
        if self.model is None:
            raise BaseException("Debes declarar el modelo del usuario")
        if not hasattr(self.model, "token"):
            raise BaseException("El modelo debe tener el campo 'token'")
        try:
            user = self.model.objects.get(token=token)
        except self.model.DoesNotExist:
            raise exceptions.AuthenticationFailed("Token invalido")

        if not user.is_active:
            raise exceptions.AuthenticationFailed("El usuario no esta activo")

        return (user, user.token)

    def authenticate_header(self, request):
        return self.keyword


class DocenteAuthentication(RefuerzamasBaseAuthentication):
    model = Docente


class EstudianteAuthentication(RefuerzamasBaseAuthentication):
    model = Estudiante
