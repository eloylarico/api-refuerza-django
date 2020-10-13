from django.apps import AppConfig


class ClasesConfig(AppConfig):
    name = "refuerzamas.clases"

    def ready(self):
        import refuerzamas.clases.signals
