from django.apps import AppConfig


class CrackersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'crackers'

    def ready(self):
        from . import handlers
