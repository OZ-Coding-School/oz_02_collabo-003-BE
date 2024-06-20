from django.apps import AppConfig

class KluckNotificationsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "kluck_notifications"
    verbose_name = "푸시 알림 자동 발송"