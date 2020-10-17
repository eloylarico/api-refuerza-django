from django.conf import settings
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from refuerzamas.clases.models import Docente, Estudiante, Mensaje, Reserva, Chat, Tutor, User
from refuerzamas.utils.pusher import PusherChannelsClient

from refuerzamas.utils.mail import enviar_correo

# User
@receiver(pre_save, sender=User)
def enviar_correo(sender, instance: User, **kwargs):
    # SI el usuario no ha sido guardado antes, no tiene una pk. Es decir si es un nuevo usuario
    if instance.pk is None and instance.tipo_usuario is not None:
        # Enviar correo de bienvenida
        enviar_correo(
            f"BIENVENIDO",
            f"""
            BIENVENIDO
            - Tu pass es: {instance._password}
            """,
            settings.DEFAULT_FROM_EMAIL,
            [instance.email],
        )
    # else:
    #     # Enviar correo de que se ha cambiado su pass o algo
    #     send_mail(
    #         f"PASS CAMBIADA",
    #         f"""
    #         PASS CAMBIADA
    #         - Tu pass es: {instance._password}
    #         """,
    #         settings.EMAIL_CONFIG.get("EMAIL_HOST_USER"),
    #         [instance.correo],
    #     )


@receiver(post_save, sender=User)
def borrar_perfil_erroneo(sender, instance: User, **kwargs):
    # SI el usuario no es del tipo, borrar su perfil, en caso exista
    if instance.tipo_usuario != User.ESTUDIANTE:
        try:
            Estudiante.objects.get(user=instance).delete()
        except Estudiante.DoesNotExist:
            pass
    if instance.tipo_usuario != User.DOCENTE:
        try:
            Docente.objects.get(user=instance).delete()
        except Docente.DoesNotExist:
            pass
    if instance.tipo_usuario != User.TUTOR:
        try:
            Tutor.objects.get(user=instance).delete()
        except Tutor.DoesNotExist:
            pass


@receiver(post_save, sender=User)
def borrar_perfil_erroneo(sender, instance: User, created, **kwargs):
    # SI el usuario no es del tipo, borrar su perfil, en caso exista
    if instance.tipo_usuario != User.ESTUDIANTE:
        try:
            Estudiante.objects.get(user=instance).delete()
        except Estudiante.DoesNotExist:
            pass
    if instance.tipo_usuario != User.DOCENTE:
        try:
            Docente.objects.get(user=instance).delete()
        except Docente.DoesNotExist:
            pass
    if instance.tipo_usuario != User.TUTOR:
        try:
            Tutor.objects.get(user=instance).delete()
        except Tutor.DoesNotExist:
            pass


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):

    if instance.tipo_usuario == User.ESTUDIANTE:
        Estudiante.objects.get_or_create(user=instance)
    elif instance.tipo_usuario == User.TUTOR:
        Tutor.objects.get_or_create(user=instance)
    elif instance.tipo_usuario == User.DOCENTE:
        Docente.objects.get_or_create(user=instance)


# RESERVA
@receiver(post_save, sender=Reserva)
def crear_chat(sender, instance: Reserva, created, **kwargs):
    if instance.estado == Reserva.PENDIENTE:
        return

    Chat.objects.get_or_create(user1=instance.docente.user, user2=instance.estudiante.user)
    Chat.objects.get_or_create(user1=instance.docente.user, user2=instance.estudiante.tutor.user)


# MENSAJE
@receiver(post_save, sender=Mensaje)
def enviar_mensaje_pusher(sender, instance: Mensaje, created, **kwargs):
    if not created:
        return
    pusher_client = PusherChannelsClient()
    pusher_client.send_chat_message(chat=instance.chat, mensaje=instance)


#
# @receiver(post_save, sender=Mensaje)
# def enviar_notificacion(sender, instance: Mensaje, created, **kwargs):
#     if not created:
#         return
#     pusher_client = PusherChannelsClient()
#     pusher_client.send_chat_message(chat=instance.chat, mensaje=instance)
