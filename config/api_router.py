from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

# Genero
# from refuerzamas.clases.api.views import DocenteViewSet
from refuerzamas.clases.api.views import (
    GenerosView,
    NivelesGradoView,
    ClasesUserViewSet,
    DocenteViewSet, ChatViewSet,
)


if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

# router.register("docentes", DocenteViewSet)
router.register(r"generos", GenerosView, basename="generos")
router.register(r"niveles", NivelesGradoView, basename="niveles")
router.register(r"clases", ClasesUserViewSet, basename="clases")

router.register(r"docentes", DocenteViewSet, basename="docentes")
router.register(r"chats", ChatViewSet, basename="chats")


app_name = "api"
urlpatterns = router.urls
