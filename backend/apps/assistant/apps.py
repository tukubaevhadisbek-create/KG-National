from django.apps import AppConfig

class AssistantConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.assistant'  # <-- Проверьте, чтобы здесь было именно 'apps.assistant'