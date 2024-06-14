from django.apps import AppConfig
from django.apps.registry import apps
from django.conf import settings
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import logging
import pytz

class GptPromptConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "gpt_prompts"
    verbose_name = "GPT API를 이용한 오늘의 한마디 데이터 자동 저장"

    def ready(self):
        # 스케줄러 초기화 다른 곳으로 옮겨 지연시키기
        self.initialize_scheduler()

    def initialize_scheduler(self):
        from .scheduler import gpt_today_job
        from admin_settings.models import AdminSetting

        # AdminSetting 테이블에서 term_time 가져오기
        try:
            scheduler_time = AdminSetting.objects.first().term_time
            # 숫자 네자리를 문자열로 변환하여 분리
            scheduler_time_str = str(scheduler_time).zfill(4)  # 네자리로 맞추기 위해 zfill 사용
            hour = int(scheduler_time_str[:2])  # 앞 두 자리
            minute = int(scheduler_time_str[2:])  # 뒤 두 자리
        except AttributeError:
            # 예외 처리: AdminSetting 객체가 없을 경우 기본값 설정
            hour = 1
            minute = 10

        scheduler = BackgroundScheduler(timezone=pytz.timezone('Asia/Seoul'))
        scheduler.add_job(
            gpt_today_job,
            trigger=CronTrigger(hour=hour, minute=minute),  # 매일 새벽 1시 10분에 실행
        )
        
        logger = logging.getLogger(__name__)

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
