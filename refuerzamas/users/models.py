from ckeditor.fields import RichTextField
from django.contrib.auth.models import AbstractUser, User
from django.core.exceptions import ValidationError
from django.db import models
from model_utils.models import TimeStampedModel

from refuerzamas.ciudades.models import Ciudad, Region, Pais


class Genero(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.nombre}"

    class Meta:
        verbose_name = "Género"
        verbose_name_plural = "Géneros"


class Nivel(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = RichTextField("Descripción", default="")
    orden = models.PositiveIntegerField(blank=True, null=True)
    foto = models.ImageField("Icono del nivel", upload_to="usuarios/niveles", null=True, blank=True)

    class Meta:
        verbose_name_plural = "Niveles"
        verbose_name = "Nivel"

    def __str__(self):
        return self.nombre


class Institucion(models.Model):
    nombre = models.CharField(max_length=255)
    ciudad = ciudad = models.ForeignKey(
        Ciudad,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text="Campo que referencia a la ciudad de la instición",
    )
    nivel = models.ForeignKey(
        Nivel,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text="Campo que referencia al nivel académico: Escolar, Preparatoria, Universidad",
    )
    foto = models.ImageField("Foto de la institucion", upload_to="usuarios/institucion", null=True, blank=True)

    def __str__(self):
        return f"{self.nombre}"

    class Meta:
        verbose_name = "Institución"
        verbose_name_plural = "Instituciones"


#
# class BaseUserAplicacion(TimeStampedModel):
#     """Usuario base para las aplicaciones de Refuerza+ (estudiante, docente)."""
#
#     # nombres = models.CharField("Nombres", blank=True, null=True, max_length=255)
#     # apellidos = models.CharField("Apellidos", blank=True, null=True, max_length=255)
#     avatar = models.ImageField("Foto de perfil", upload_to="users/avatar", null=True, blank=True)
#     fecha_nacimiento = models.DateField("Fecha de nacimiento", null=True, blank=True)
#     genero = models.ForeignKey(Genero, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Género")
#     celular = models.CharField(max_length=9, null=True, blank=True)
#     # usuario_aplicacion = models.CharField(
#     #     "Nombre de usuario",
#     #     max_length=50,
#     #     unique=True,
#     #     help_text="Nombre de usuario con el cual el usuario entrará a la aplicación",
#     # )
#     # codigo_aplicacion = models.CharField(
#     #     "Código de usuario", max_length=15, help_text="Código con el cual el usuario entrará a la aplicación"
#     # )
#     email = models.EmailField("Correo electrónico", unique=True)
#     ciudad = models.ForeignKey(
#         Ciudad,
#         on_delete=models.CASCADE,
#         null=True,
#         blank=True,
#         help_text="Campo que referencia a la ciudad del usuario en la aplicación",
#     )
#
#     @property
#     def nombre_completo(self):
#         return f"{self.nombres} {self.apellidos}"
#
#     def __str__(self):
#         return self.nombre_completo
#
#     class Meta:
#         abstract = True


class User(AbstractUser):
    """Default user para RefuerzaMas."""

    TIPO_USUARIO_CHOICES = [
        ("ESTUDIANTE", "Estudiante"),
        ("PROFESOR", "Profesor"),
        ("TUTOR", "Tutor"),
    ]
    avatar = models.ImageField("Foto de perfil", upload_to="users/avatar", null=True, blank=True)
    fecha_nacimiento = models.DateField("Fecha de nacimiento", null=True, blank=True)
    genero = models.ForeignKey(Genero, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Género")
    celular = models.CharField(max_length=9, null=True, blank=True)
    tipo_usuario = models.CharField(max_length=100, choices=TIPO_USUARIO_CHOICES, blank=True, null=True)
    email = models.EmailField("Correo electrónico", unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    @property
    def nombre_completo(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.username or self.email

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"


class Estudiante(models.Model):
    """
    Modelo Estudiante que tiene todos los campos de BaseUserAplicación mas los que se declaran acá
    """

    user = models.OneToOneField(User, on_delete=models.PROTECT, related_name="perfil_estudiante")
    institucion = models.ForeignKey(Institucion, on_delete=models.PROTECT, null=True, blank=True)
    ciclo_universidad = models.PositiveIntegerField(blank=True, null=True, default=0)
    grado_colegio = models.PositiveIntegerField(blank=True, null=True, default=0)


class Docente(models.Model):
    """
    Modelo docente que tiene todos los campos de BaseUserAplicación
    """

    user = models.OneToOneField(User, on_delete=models.PROTECT, related_name="perfil_docente")
    breve_cv = RichTextField(null=True, blank=True)
    filosofia = RichTextField(null=True, blank=True)


class HorarioLibreDocente(models.Model):

    docente = models.ForeignKey(
        Docente,
        on_delete=models.CASCADE,
        verbose_name="Horarios Libres del Docente",
    )
    hora_inicio = models.DateTimeField("Fecha y hora del inicio del horario libre")
    hora_fin = models.DateTimeField("Fecha y hora del fin del horario libre")

    def clean(self) -> None:
        if self.hora_inicio > self.hora_fin:
            raise ValidationError("La hora de inicio no puede ser mayor a la hora de fin")

    def __str__(self):
        return f"{self.docente} [{self.hora_inicio} - {self.hora_fin}]"

    class Meta:
        verbose_name = "Horario Libre"
        verbose_name_plural = "Horarios Libres"
