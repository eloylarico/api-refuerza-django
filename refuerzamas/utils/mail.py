import functools

from django.core.mail import send_mail as django_send_mail
import asyncio

loop = asyncio.get_event_loop()


def send_mail(*args, **kwargs):
    loop.run_in_executor(None, functools.partial(django_send_mail, *args, **kwargs))
