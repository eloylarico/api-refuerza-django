from django.conf import settings
from django.core import mail
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from refuerzamas.clases.api.serializers import ClaseModelSerializer
from refuerzamas.clases.models import Docente, Estudiante, Mensaje, Reserva, Chat, Tutor, User, Clase
from refuerzamas.utils.pusher import PusherBeamsClient, PusherChannelsClient

from refuerzamas.utils.mail import send_mail


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
    if instance.estudiante.tutor is not None:
        Chat.objects.get_or_create(user1=instance.docente.user, user2=instance.estudiante.tutor.user)


@receiver(post_save, sender=Reserva)
def enviar_señal_clase_reservada(sender, instance: Reserva, created, **kwargs):
    if instance.estado == Reserva.ACTIVA:
        pusher_client = PusherChannelsClient()
        pusher_client.send_class_reserved(reserva=instance)


@receiver(post_save, sender=Reserva)
def enviar_señal_docentes(sender, instance: Reserva, created, **kwargs):
    if instance.estado == Reserva.PENDIENTE:
        pusher_client = PusherChannelsClient()
        pusher_client.send_new_class_alert(reserva=instance)


@receiver(post_save, sender=Reserva)
def enviar_notificaciones_docentes(sender, instance: Reserva, created, **kwargs):
    if instance.estado == Reserva.PENDIENTE:
        body = f"Hay una nueva clase disponible de {instance.curso.materia.nombre}"
        pusher_beams_client = PusherBeamsClient()
        pusher_beams_client.send_notification_to_interests(
            interests=[f"curso-{instance.curso_id}"], title="Nueva clase disponible", body=body
        )


@receiver(post_save, sender=Reserva)
def enviar_correo_alumno(sender, instance: Reserva, created, **kwargs):
    if instance.estado == Reserva.ACTIVA:
        subject = "Clase confirmada - Refuerza+"
        html_message = render_to_string(
            "mail/clase_confirmada_alumno.html",
            {
                "reserva": instance,
                "estudiante": instance.estudiante.user,
                "docente": instance.docente.user,
            },
        )
        plain_message = strip_tags(html_message)
        from_email = settings.DEFAULT_FROM_EMAIL
        to = instance.estudiante.user.email
        # mail.send_mail(
        #     subject=subject,
        #     message=plain_message,
        #     from_email=from_email,
        #     recipient_list=[to],
        #     html_message=html_message,
        # )
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=from_email,
            recipient_list=[to],
            html_message=html_message,
        )


@receiver(post_save, sender=Reserva)
def enviar_correo_docente(sender, instance: Reserva, created, **kwargs):
    if instance.estado == Reserva.ACTIVA:
        subject = "Clase confirmada - Refuerza+"
        html_message = render_to_string(
            "mail/clase_confirmada_docente.html",
            {
                "reserva": instance,
                "estudiante": instance.estudiante.user,
                "docente": instance.docente.user,
            },
        )
        plain_message = strip_tags(html_message)
        from_email = settings.DEFAULT_FROM_EMAIL
        to = instance.docente.user.email
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=from_email,
            recipient_list=[to],
            html_message=html_message,
        )


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
