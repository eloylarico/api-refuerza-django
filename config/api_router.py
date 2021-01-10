from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

# Genero
# from refuerzamas.clases.api.views import DocenteViewSet
from refuerzamas.clases.api.views import (
    EstudianteViewSet,
    GenerosView,
    NivelesGradoView,
    ClasesUserViewSet,
    DocenteViewSet,
    ChatViewSet,
    MensajeViewSet,
    ReservaViewSet,
    DiaViewSet,
    TiposPagoViewSet,
    OrdenCompraViewSet,
)
from refuerzamas.clases.api.views.instituciones import InstitucionViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

# router.register("docentes", DocenteViewSet)
router.register(r"generos", GenerosView, basename="generos")
router.register(r"niveles", NivelesGradoView, basename="niveles")
router.register(r"clases", ClasesUserViewSet, basename="clases")
router.register(r"reservas", ReservaViewSet, basename="reservas")

router.register(r"docentes", DocenteViewSet, basename="docentes")
router.register(r"estudiantes", EstudianteViewSet, basename="estudiantes")
router.register(r"chats", ChatViewSet, basename="chats")
router.register(r"mensajes", MensajeViewSet, basename="mensajes")
router.register(r"instituciones", InstitucionViewSet, basename="instituciones")
router.register(r"dias", DiaViewSet, basename="dias")
router.register(r"tipos_pago", TiposPagoViewSet, basename="tipo_pago")
router.register(r"orden_compra", OrdenCompraViewSet, basename="orden_compra")


app_name = "api"
urlpatterns = router.urls
