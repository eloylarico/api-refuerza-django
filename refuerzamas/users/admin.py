from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.admin.decorators import register
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from refuerzamas.users.models import Docente, Estudiante, Genero, HorarioLibreDocente, Institucion, Nivel


@register(Estudiante)
class EstudianteAdmin(ModelAdmin):
    list_display = [
        "user",
        "ciclo_universidad",
        "grado_colegio",
    ]
    list_filter = [
        "user__genero",
        "institucion",
    ]
    search_fields = [
        "user__first_name",
        "user__last_name",
        "user__email",
        "user__celular",
    ]


class HorarioLibreDocenteAdmin(admin.TabularInline):
    list_display = ["docente", "hora_inicio", "hora_fin"]
    model = HorarioLibreDocente
    extra = 1


@register(Docente)
class DocenteAdmin(ModelAdmin):
    inlines = [HorarioLibreDocenteAdmin]
    list_display = [
        "user",
        "breve_cv",
        "filosofia",
    ]
    list_filter = [
        "user__genero",
    ]
    search_fields = [
        "user__first_name",
        "user__last_name",
        "user__email",
        "user__celular",
    ]


@register(Nivel)
class NivelAdmin(ModelAdmin):
    list_display = [
        "nombre",
        "descripcion",
        "orden",
    ]
    search_fields = [
        "nombre",
        "descripcion",
    ]


@register(Genero)
class GeneroAdmin(ModelAdmin):
    list_display = [
        "nombre",
    ]
    search_fields = [
        "nombre",
    ]


@register(Institucion)
class InstitucionAdmin(ModelAdmin):
    list_display = [
        "nombre",
        "ciudad",
    ]
    list_filter = [
        "ciudad",
        "nivel",
    ]
    search_fields = [
        "nombre",
    ]


# Modifica los campos del administrador del usuario
UserAdmin.fieldsets = ((None, {"fields": ("username", "password")}),)
UserAdmin.fieldsets += (
    (
        "Información Personal",
        {
            "fields": (
                "first_name",
                "last_name",
                "email",
                "celular",
                "fecha_nacimiento",
                "avatar",
                "genero",
                "tipo_usuario",
            )
        },
    ),
)
UserAdmin.fieldsets += (("Permisos", {"classes": ("collapse",), "fields": ("is_active", "is_staff", "is_superuser")}),)
UserAdmin.fieldsets += (
    (
        "Fechas Importantes",
        {
            "classes": ("collapse",),
            "fields": (
                "last_login",
                "date_joined",
            ),
        },
    ),
)
UserAdmin.ordering = ("-id",)
UserAdmin.list_filter += ("genero",)
UserAdmin.list_display = (
    "username",
    "first_name",
    "last_name",
    "email",
    "is_staff",
    "is_active",
)

User = get_user_model()
admin.site.register(User, UserAdmin)

# admin.site.register(User, UserAdmin)
