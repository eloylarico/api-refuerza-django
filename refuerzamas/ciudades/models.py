from django.db import models


class Pais(models.Model):
    nombre = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Países"
        verbose_name = "País"

    def __str__(self):
        return self.nombre


class Region(models.Model):
    nombre = models.CharField(max_length=100)
    pais = models.ForeignKey(
        Pais,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="País",
        help_text="Campo que referencia al País de la región",
    )

    class Meta:
        verbose_name_plural = "Regiones"
        verbose_name = "Región"

    def __str__(self):
        return self.nombre


class Ciudad(models.Model):
    nombre = models.CharField(max_length=100)
    region = models.ForeignKey(
        Region,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Ciudad",
        help_text="Campo que referencia la región de la ciudad",
    )

    class Meta:
        verbose_name_plural = "Ciudades"
        verbose_name = "Ciudad"

    def __str__(self):
        return self.nombre
