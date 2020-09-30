from django.contrib import admin

# Register your models here.
from django.contrib.admin import ModelAdmin
from django.contrib.admin.decorators import register

from refuerzamas.ciudades.models import Ciudad, Pais, Region


@register(Ciudad)
class CiudadAdmin(ModelAdmin):
    list_display = [
        "nombre",
        "region",
    ]
    list_filter = [
        "region",
    ]
    search_fields = [
        "nombre",
    ]
    ordering = ["-id"]


@register(Region)
class RegionAdmin(ModelAdmin):
    list_display = [
        "nombre",
        "pais",
    ]
    list_filter = [
        "pais",
    ]
    search_fields = [
        "nombre",
    ]
    ordering = ["-id"]


@register(Pais)
class PaisAdmin(ModelAdmin):
    list_display = [
        "nombre",
    ]
    search_fields = [
        "nombre",
    ]
    ordering = ["-id"]
