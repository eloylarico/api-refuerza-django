from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

# Genero
# from refuerzamas.clases.api.views import DocenteViewSet
from refuerzamas.clases.api.views import GenerosView, NivelesView, NivelesGradoView, ClasesUserViewSet, DocenteViewSet


if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

# router.register("docentes", DocenteViewSet)
router.register('generos', GenerosView)
router.register('niveles', NivelesView)
router.register('niveles/(?P<id>[0-9]+)/grados', NivelesGradoView)
router.register(r'clases',ClasesUserViewSet)
router.register(r'docentes', DocenteViewSet)



app_name = "api"
urlpatterns = router.urls
