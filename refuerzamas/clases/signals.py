from django.db.models.signals import post_save
from django.dispatch import receiver

from refuerzamas.clases.models import Reserva, Chat


@receiver(post_save, sender=Reserva)
def crear_chat(sender, instance: Reserva, created, **kwargs):
    if instance.estado == Reserva.PENDIENTE:
        return

    Chat.objects.get_or_create(user1=instance.docente.user, user2=instance.estudiante.user)
    Chat.objects.get_or_create(user1=instance.docente.user, user2=instance.estudiante.tutor.user)
