from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

# from refuerzamas.clases.api.views import DocenteViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

# router.register("docentes", DocenteViewSet)


app_name = "api"
urlpatterns = router.urls
