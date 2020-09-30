from django.db import models


class ClasesManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().exclude(docente__isnull=True)
