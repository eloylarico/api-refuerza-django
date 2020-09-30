# Register your models here.
from django.contrib.admin import ModelAdmin
from django.contrib.admin.decorators import register
from django.db.models import QuerySet
from django.http import HttpRequest

from refuerzamas.clases.models import Clase, Curso, Estado, Reserva


@register(Reserva)
class ReservaAdmin(ModelAdmin):
    list_display = [
        "estudiante",
        "docente",
        "curso",
        "estado",
        "hora_inicio",
        "hora_fin",
        "precio",
    ]
    autocomplete_fields = [
        "estudiante",
        "docente",
    ]
    list_filter = [
        "estado",
        "curso",
        "curso__nivel",
        "docente",
    ]
    search_fields = [
        "estudiante",
        "docente",
        "curso",
    ]
    ordering = ["-id"]


@register(Clase)
class ClasesAdmin(ModelAdmin):

    list_display = [
        "estudiante",
        "docente",
        "curso",
        "estado",
        "hora_inicio",
        "hora_fin",
        "precio",
    ]
    autocomplete_fields = [
        "estudiante",
        "docente",
    ]
    list_filter = [
        "estado",
        "curso",
        "curso__nivel",
        "docente",
    ]
    search_fields = [
        "estudiante",
        "docente",
        "curso",
    ]
    ordering = ["-id"]

    def has_add_permission(self, request, obj=None) -> bool:
        return False

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        return Clase.clases


@register(Estado)
class EstadoAdmin(ModelAdmin):
    list_display = [
        "nombre",
        "orden",
    ]
    search_fields = [
        "nombre",
    ]
    ordering = ["-id"]


@register(Curso)
class CursoAdmin(ModelAdmin):
    list_display = [
        "nombre",
        "nivel",
    ]
    search_fields = [
        "nombre",
        "nivel",
    ]
    list_filter = [
        "nivel",
    ]
    ordering = ["-id"]
