from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

# Genero
# from refuerzamas.clases.api.views import DocenteViewSet
from refuerzamas.clases.api.views import GenerosView, NivelesView, NivelesGradoView, UserView


if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

# router.register("docentes", DocenteViewSet)
#router.register("auth/user/", UserView)

router.register('genero', GenerosView)

router.register('nivel', NivelesView)
router.register('nivel/(?P<id>[0-9]+)/grado', NivelesGradoView)



app_name = "api"
urlpatterns = router.urls
