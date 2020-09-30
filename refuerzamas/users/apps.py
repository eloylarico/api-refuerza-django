from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "refuerzamas.users"
    verbose_name = "Usuarios"

    def ready(self):
        try:
            import refuerzamas.users.signals  # noqa F401
        except ImportError:
            pass
