from django.apps import AppConfig
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import logging
import pytz


# 푸시 로거 가져오기
push_logger = logging.getLogger('push_jobs')

class KluckNotificationsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "kluck_notifications"
    verbose_name = "푸시 알림 자동 발송"

    def ready(self):
        from admin_settings.models import AdminSetting
        from .push_scheduler import send_push_notifications, remove_inactive_tokens
            
        try:
            # AdminSetting 테이블에서 push_time 가져오기
            push_time = AdminSetting.objects.first().push_time
            # 숫자 네자리를 문자열로 변환하여 분리
            push_time_str = str(push_time).zfill(4)  # 네자리로 맞추기 위해 zfill 사용
            hour = int(push_time_str[:2])  # 앞 두 자리
            minute = int(push_time_str[2:])  # 뒤 두 자리
        except AttributeError:
            # 예외 처리: AdminSetting 객체가 없을 경우 기본값 설정
            push_logger.warning("AdminSetting 객체가 없어 기본값으로 설정합니다.")
            hour = 8
            minute = 0


        push_scheduler = BackgroundScheduler(timezone=pytz.timezone('Asia/Seoul'))
        push_scheduler.add_job(
            send_push_notifications, # 푸시 알림 보내기
            trigger=CronTrigger(hour=hour, minute=minute), # 설정된 push_time에 실행
        )
        push_scheduler.add_job(
            remove_inactive_tokens, # 비활성화 토큰 삭제
            trigger=CronTrigger(hour=0, minute=0),  # 매일 자정에 실행
        )

        try:
            push_logger.info("Starting Push scheduler...")
            push_scheduler.start()
        except KeyboardInterrupt:
            push_logger.warning("Stopping Push scheduler...")
            push_scheduler.shutdown()
            push_logger.warning("Push scheduler shut down successfully!")