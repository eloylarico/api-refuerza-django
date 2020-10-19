from typing import List

from django.conf import settings
import pusher
from pusher_push_notifications import PushNotifications
from rest_framework.request import Request

from refuerzamas.clases.api.serializers import ClaseModelSerializer, MensajeModelSerializer
from refuerzamas.clases.models import Chat, Mensaje, Reserva


def load_pusher_channels_config():
    pusher_channels_app_id = settings.PUSHER_CHANNELS_APP_ID
    pusher_channels_key = settings.PUSHER_CHANNELS_KEY
    pusher_channels_secret = settings.PUSHER_CHANNELS_SECRET
    pusher_channels_cluster = settings.PUSHER_CHANNELS_CLUSTER
    return pusher_channels_app_id, pusher_channels_key, pusher_channels_secret, pusher_channels_cluster


def load_pusher_beams_config():
    pusher_beams_instance_id = settings.PUSHER_BEAMS_INSTANCE_ID
    pusher_beams_secret_key = settings.PUSHER_BEAMS_SECRET_KEY
    return pusher_beams_instance_id, pusher_beams_secret_key


class PusherChannelsClient:
    def __init__(self):
        (
            pusher_channels_app_id,
            pusher_channels_key,
            pusher_channels_secret,
            pusher_channels_cluster,
        ) = load_pusher_channels_config()

        self.pusher_client = pusher.Pusher(
            app_id=pusher_channels_app_id,
            key=pusher_channels_key,
            secret=pusher_channels_secret,
            cluster=pusher_channels_cluster,
            ssl=True,
        )

    def send_chat_message(self, chat: Chat, mensaje: Mensaje):
        canal = f"chat-{chat.id}"
        mensaje = MensajeModelSerializer(mensaje)
        self.pusher_client.trigger(canal, "mensaje", mensaje.data)

    def send_new_class_alert(self, reserva: Reserva):
        canal = f"clase-curso-{reserva.curso_id}"
        reserva = ClaseModelSerializer(reserva)
        self.pusher_client.trigger(canal, "clase_disponible", reserva.data)


class PusherBeamsClient:
    def __init__(self):
        (
            pusher_beams_instance_id,
            pusher_beams_secret_key,
        ) = load_pusher_beams_config()

        self.pusher_beams_client = PushNotifications(
            instance_id=pusher_beams_instance_id,
            secret_key=pusher_beams_secret_key,
        )

    def send_notification_to_interests(self, interests: List[str], title: str, body: str):
        publish_body = {
            "apns": {
                "aps": {
                    "alert": {
                        "title": title,
                        "body": body,
                    },
                },
            },
            "fcm": {
                "notification": {
                    "title": title,
                    "body": body,
                },
            },
            "web": {
                "notification": {
                    "title": title,
                    "body": body,
                },
            },
        }
        self.pusher_beams_client.publish_to_interests(interests, publish_body)
