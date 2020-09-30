from django.core.exceptions import ValidationError
from django.db import models

# Create your models here.
from refuerzamas.clases.managers import ClasesManager
from refuerzamas.users.models import Docente, Estudiante, Nivel


class Estado(models.Model):
    # Campos
    nombre = models.CharField(max_length=100)
    orden = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Estado de la Reserva"
        verbose_name_plural = "Estados de la Reserva"


class Curso(models.Model):
    nombre = models.CharField(max_length=100)
    nivel = models.ForeignKey(
        Nivel,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Nivel",
        help_text="Campo que referencia al nivel académico: Escolar, Preparatoria, Universidad",
    )
    foto = models.ImageField("Ícono del curso", upload_to="clases/cursos/fotos", null=True)

    class Meta:
        verbose_name_plural = "Cursos"
        verbose_name = "Curso"

    def __str__(self):
        return self.nombre


class Reserva(models.Model):
    # Campos

    estudiante = models.ForeignKey(Estudiante, on_delete=models.PROTECT, verbose_name="Estudiante")
    """ Se le coloca clases como related name, ya que si un profesor tiene reservas es porque esa reverva paso a ser clases """
    docente = models.ForeignKey(Docente, on_delete=models.PROTECT, null=True, blank=True, related_name="clases")
    precio = models.FloatField("Precio al Estudiante")
    hora_inicio = models.DateTimeField()
    hora_fin = models.DateTimeField()
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name="reservas")
    estado = models.ForeignKey(Estado, on_delete=models.PROTECT, help_text="Estado de la reserva")

    class Meta:
        verbose_name = "Reserva"
        verbose_name_plural = "Reservas"

    def clean(self) -> None:
        if self.hora_inicio > self.hora_fin:
            raise ValidationError("La hora de inicio no puede ser mayor a la hora de fin")

    def __str__(self):
        return f"Reserva de {self.estudiante} | Curso: + {self.curso} | Estado: {self.estado}"


class Clase(Reserva):
    """
    Modelo proxy para poder tener en el admin de django "Clase", el cuál traerá todas las reservas
    con un profesor asignado (a través del manager clases)"
    """

    clases = ClasesManager()

    class Meta:
        proxy = True
        verbose_name = "Clase"
        verbose_name_plural = "Clases"
