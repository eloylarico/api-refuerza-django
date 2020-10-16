from django.core.mail import send_mail
import asyncio

loop = asyncio.get_event_loop()


def enviar_correo(*args):
    send_mail(*args)
    # loop.run_in_executor(
    #     None,
    #     send_mail,
    #     *args,
    # )
