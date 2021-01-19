# Rest
from django.http import Http404
from rest_framework import mixins, viewsets, status

# Serializer
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from django.core.exceptions import ValidationError as ModelValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from refuerzamas.clases.api.serializers import (
    ClaseModelSerializer,
    ReservaModelSerializer,
    DiaModelSerializer,
    TextoPagoSerializer,
    TipoPagoModelSerializer,
)

# Model
from refuerzamas.clases.models import (
    Clase,
    User,
    Reserva,
    Dia,
    TipoPago,
    CodigoDescuento,
)


class ClasesUserViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = ClaseModelSerializer

    def get_queryset(self):
        if self.request.user.tipo_usuario == User.ESTUDIANTE:
            return Clase.clases.filter(estado=Reserva.ACTIVA, estudiante=self.request.user.perfil_estudiante)

        elif self.request.user.tipo_usuario == User.DOCENTE:
            return Clase.clases.filter(estado=Reserva.ACTIVA, docente=self.request.user.perfil_docente)

        elif self.request.user.tipo_usuario == User.TUTOR:
            return Clase.clases.filter(
                estado=Reserva.ACTIVA, estudiante__tutor=self.request.user.perfil_tutor
            ).distinct()


class ReservaViewSet(viewsets.GenericViewSet):
    serializer_class = ClaseModelSerializer
    queryset = Reserva.objects.all()

    @action(detail=True, methods=["POST"])
    def tomar(self, request, pk=None):
        try:
            user = self.request.user
            reserva = self.get_object()
            reserva.asignar(user.perfil_docente.id)
            serializer = self.get_serializer(reserva)
        except ModelValidationError:
            raise ValidationError("Esta clase ya ha sido tomada")
        return Response(serializer.data)

    @action(detail=False, methods=["GET"])
    def ultimo(self, request):
        user = self.request.user
        cursos = user.perfil_docente.cursos.values_list("id", flat=True)
        reserva = Reserva.objects.filter(curso_id__in=cursos, estado=Reserva.PENDIENTE).last()
        serializer = ClaseModelSerializer(reserva)
        return Response(serializer.data)

    @action(detail=False, methods=["GET"])
    def mis_reservas(self, request):
        user = self.request.user
        if user.tipo_usuario == User.ESTUDIANTE or user.tipo_usuario == User.TUTOR:
            mis_reservas = user.get_mis_reservas()
            serializer = ReservaModelSerializer(mis_reservas, many=True)
            return Response(serializer.data)

        return Response(None, status=status.HTTP_204_NO_CONTENT)


class DiaViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Dia.objects.all()
    serializer_class = DiaModelSerializer


class TiposPagoViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = TipoPago.objects.all()
    serializer_class = TipoPagoModelSerializer


class OrdenCompraViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = ClaseModelSerializer
    queryset = Reserva.objects.all()

    def create(self, request, *args, **kwargs):
        user = request.user
        if user.tipo_usuario == User.ESTUDIANTE or user.tipo_usuario == User.TUTOR:
            curso_id = request.data.get("curso_id")
            docente_id = request.data.get("docente_id")
            fechas = request.data.get("fechas")
            estudiante_id = request.data.get("estudiante_id", False)  # El usuario tutor envía este parametro
            compra = user.crear_orden(curso_id, docente_id, fechas, estudiante_id)
            serializer = ReservaModelSerializer(compra, many=True)
            return Response(serializer.data)

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=["GET"])
    def ver_orden(self, request):
        codigo_compra = request.query_params.get("codigo_compra", False)
        reservas = Reserva.objects.filter(orden_compra=codigo_compra)
        serializer = ReservaModelSerializer(reservas, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["POST"])
    def aplicar_codigo_descuento(self, request):
        codigo = request.data.get("codigo_descuento")
        codigo_compra = request.data.get("codigo_compra")
        reservas = Reserva.objects.filter(orden_compra=codigo_compra)
        compra = []
        codigo_descuento = get_object_or_404(CodigoDescuento, codigo=codigo)
        for reserva in reservas:
            reserva.aplicar_codigo_descuento(codigo_descuento)
            compra.append(reserva)
        serializer = ReservaModelSerializer(compra, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["POST"])
    def adjuntar_comprobante_pago(self, request):
        codigo_compra = request.data.get("codigo_compra")
        foto_comprobante = request.data.get("foto_comprobante")
        medio_pago_id = request.data.get("medio_pago_id")
        reservas = Reserva.objects.filter(orden_compra=codigo_compra)
        for reserva in reservas:
            reserva.adjuntar_comprobante_pago(foto_comprobante, medio_pago_id)
        return Response(None, status=status.HTTP_200_OK)

    @action(detail=False, methods=["POST"])
    def adjuntar_texto_pago(self, request):
        # texto_pago = request.data.get("texto_pago")
        serializer = TextoPagoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        nombre_foto = data.pop("nombre_foto")
        reservas = serializer.context.get("reservas_asociadas")
        for reserva in reservas:
            reserva.adjuntar_texto_pago(**data)
        return Response(None, status=status.HTTP_204_NO_CONTENT)
