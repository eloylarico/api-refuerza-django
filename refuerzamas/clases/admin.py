# Register your models here.
from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.admin.decorators import register
from django.contrib.admin import widgets as admin_widgets
from django.contrib.auth.admin import UserAdmin
from django.db import models
from django.db.models import QuerySet

# form django.contrib.
from django.forms import widgets
from django.http import HttpRequest

from refuerzamas.clases.models import (
    Clase,
    Curso,
    Genero,
    Grado,
    HorarioLibreDocente,
    Institucion,
    Materia,
    MedioPago,
    Nivel,
    Docente,
    Estudiante,
    Tutor,
    Reserva,
    User, Chat, Mensaje,
)


@register(User)
class CustomUserAdmin(UserAdmin):
    list_display = (
        "email",
        "first_name",
        "last_name",
        "nickname",
        "ciudad",
        "email",
        "is_staff",
    )
    list_filter = (
        "genero",
        "is_staff",
        "is_superuser",
        "is_active",
        "groups",
    )
    search_fields = (
        "username",
        "first_name",
        "last_name",
        "email",
        "nickname",
        "observaciones",
        "direccion",
    )

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "username",
                    "password",
                ),
            },
        ),
        (
            "Informacion Personal",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                ),
            },
        ),
        (
            "Informacion de la aplicación",
            {
                "fields": (
                    "tipo_usuario",
                    "avatar",
                    "fecha_nacimiento",
                    "genero",
                    "celular",
                    "ciudad",
                    "direccion",
                    "observaciones",
                ),
            },
        ),
        (
            "Permisos",
            {
                "classes": ("collapse",),
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (
            "Fechas importantes",
            {
                "classes": ("collapse",),
                "fields": ("last_login", "date_joined"),
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "username",
                    "password1",
                    "password2",
                    "tipo_usuario",
                ),
            },
        ),
    )


class HorarioLibreDocenteInlineAdmin(admin.TabularInline):
    list_display = ["docente", "hora_inicio", "hora_fin"]
    model = HorarioLibreDocente
    extra = 1


@register(Docente)
class PerfilDocenteAdmin(ModelAdmin):
    inlines = [HorarioLibreDocenteInlineAdmin]
    readonly_fields = ["user"]
    list_display = [
        "user",
        "breve_cv",
        "filosofia",
    ]
    list_filter = [
        "user__genero",
        "user__ciudad",
    ]
    search_fields = [
        "user__first_name",
        "user__last_name",
        "user__nickname",
        "user__email",
        "user__celular",
        "user__nickname",
        "user__observaciones",
        "user__direccion",
    ]
    filter_horizontal = ["cursos"]

    def has_add_permission(self, request, obj=None) -> bool:
        return False


@register(Estudiante)
class PerfilEstudianteAdmin(ModelAdmin):
    readonly_fields = ["user"]
    autocomplete_fields = ["tutor"]
    list_display = [
        "user",
    ]
    list_filter = [
        "user__genero",
        "user__ciudad",
    ]
    search_fields = [
        "user__first_name",
        "user__last_name",
        "user__nickname",
        "user__email",
        "user__celular",
        "user__nickname",
        "user__observaciones",
        "user__direccion",
    ]

    def has_add_permission(self, request, obj=None) -> bool:
        return False


class TuteladosInlineAdmin(admin.TabularInline):
    verbose_name = "Tutelado"
    verbose_name_plural = "Tutelados"
    readonly_fields = ["user", "institucion", "grado"]
    model = Estudiante
    extra = 0
    max_num = 0
    can_delete = False


@register(Tutor)
class PerfilTutorAdmin(ModelAdmin):
    inlines = [TuteladosInlineAdmin]
    readonly_fields = ["user"]
    list_display = [
        "user",
    ]
    list_filter = [
        "user__genero",
        "user__ciudad",
    ]
    search_fields = [
        "user__first_name",
        "user__last_name",
        "user__nickname",
        "user__email",
        "user__celular",
        "user__nickname",
        "user__observaciones",
        "user__direccion",
    ]

    def has_add_permission(self, request, obj=None) -> bool:
        return False


class GradoInlineAdmin(admin.TabularInline):
    model = Grado
    extra = 1


@register(Nivel)
class NivelAdmin(ModelAdmin):
    inlines = [GradoInlineAdmin]
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


@register(MedioPago)
class MedioPagoAdmin(ModelAdmin):
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


@register(Reserva)
class ReservaAdmin(ModelAdmin):
    list_display = [
        "estudiante",
        "docente",
        "curso",
        "estado",
        "hora_inicio",
        "hora_fin",
        "precio_estudiante",
        "precio_docente",
    ]
    autocomplete_fields = [
        "estudiante",
        "docente",
        "curso",
        "medio_pago",
    ]
    list_filter = [
        "estado",
        "curso",
        "curso__grado",
        "docente",
    ]
    search_fields = [
        "estudiante__user__first_name",
        "estudiante__user__last_name",
        "docente__user__first_name",
        "docente__user__last_name",
        "curso__materia__nombre",
    ]
    # formfield_overrides = {
    #     models.TimeField: {"widget": admin_widgets.AdminSplitDateTime(time_format="%H:%M")},
    # }
    # formfield_overrides = {
    #     models.DateTimeField: {"widget": admin_widgets.AdminSplitDateTime(attrs={"time_format": "%H:%M"})},
    # }
    # formfield_overrides = {
    #     models.DateTimeField: {"widget": widgets.SplitDateTimeWidget(time_format="%H:%M")},
    # }


@register(Clase)
class ClasesAdmin(ModelAdmin):
    list_display = [
        "estudiante",
        "docente",
        "curso",
        "estado",
        "hora_inicio",
        "hora_fin",
        "precio_estudiante",
        "precio_docente",
    ]
    autocomplete_fields = [
        "estudiante",
        "docente",
        "curso",
        "medio_pago",
    ]
    list_filter = [
        "estado",
        "curso",
        "curso__grado",
        "docente",
    ]
    search_fields = [
        "estudiante__user__first_name",
        "estudiante__user__last_name",
        "docente__user__first_name",
        "docente__user__last_name",
        "curso__materia__nombre",
    ]

    def has_add_permission(self, request, obj=None) -> bool:
        return False

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        return Clase.clases


class CursosInlineAdmin(admin.TabularInline):
    model = Curso
    extra = 1


@register(Materia)
class MateriaAdmin(ModelAdmin):
    inlines = [CursosInlineAdmin]
    list_display = [
        "nombre",
    ]
    search_fields = [
        "nombre",
    ]


@register(Curso)
class CursoAdmin(ModelAdmin):
    list_display = [
        "materia",
        "grado",
    ]
    list_filter = [
        "materia",
        "grado",
        "grado__nivel",
    ]
    search_fields = [
        "nombre",
        "materia__nombre",
        "grado__nombre",
        "grado__nivel__nombre",
    ]



class MensajeInlineAdmin(admin.TabularInline):
    model = Mensaje
    extra = 1


@register(Chat)
class ChatAdmin(ModelAdmin):
    inlines = [MensajeInlineAdmin]
    list_display = [
        "user1",
        "user2",
    ]

# @register(Mensaje)
# class MensajeAdmin(ModelAdmin):
#     list_display = [
#         "user",
#         "chat",
#         "texto",
#     ]
