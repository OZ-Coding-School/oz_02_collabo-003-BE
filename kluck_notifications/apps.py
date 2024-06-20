from django.apps import AppConfig


#
# # 푸시 로거 가져오기
# push_logger = logging.getLogger('push_jobs')

class KluckNotificationsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "kluck_notifications"
    verbose_name = "푸시 알림 자동 발송"