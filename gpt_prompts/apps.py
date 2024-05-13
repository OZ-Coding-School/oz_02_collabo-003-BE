from django.apps import AppConfig
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
        from .scheduler import gpt_today_job

        scheduler = BackgroundScheduler(timezone=pytz.timezone('Asia/Seoul'))
        scheduler.add_job(
            gpt_today_job,
            trigger=CronTrigger(hour=18, minute=30),  # 매일 새벽 1시에 실행
        )
        
        logger = logging.getLogger(__name__)

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
