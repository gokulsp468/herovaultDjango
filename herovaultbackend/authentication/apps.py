from django.apps import AppConfig


class AuthenticationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'authentication'
    
    
    def ready(self):
        # This will import your signals module when the app is ready
        import authentication.signals
