from django.apps import AppConfig
class StuhelperAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'stuhelper_app'

    def ready(self):
        from session.token import create_token_auto_clear_thread
        create_token_auto_clear_thread()
