from django.apps import AppConfig

class GymmyConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'gymmy'

    def ready(self):
        import gymmy.signals
