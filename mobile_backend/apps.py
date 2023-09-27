from django.apps import AppConfig


class MobileBackendConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mobile_backend'

    def ready(self):
        import mobile_backend.signals
