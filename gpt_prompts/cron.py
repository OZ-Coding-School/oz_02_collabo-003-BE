from django.utils import timezone
from datetime import datetime
from .scheduler import gpt_today_job
from admin_settings.models import AdminSetting
import logging
import pytz

logger = logging.getLogger('gpt_jobs')

def gpt_cron_job():
    """
    매분마다 관리자 페이지에서 설정한 term_time과 현재 시각(한국 기준)을 비교한 후, 
    현재 시각이 term_time이면 gpt_prompts를 돌려 운세를 생산하고, term_time이 아니라면 운세를 생산하지 않는다.
    """

    # DB에서 term_time 가져오기
    try:
        term_time = AdminSetting.objects.first().term_time
    except AttributeError:
        term_time = "0110" # 기본값 새벽 1시 10분

    # 현재 시각
    current_time = datetime.now(pytz.timezone('Asia/Seoul'))
    # 현재 시각과 push_time 같은 형식으로 맞추기
    current_time_str = current_time.strftime('%H%M')

    # 현재 시각과 push_time이 같으면 푸시 발송
    if current_time_str == term_time:
        gpt_today_job()
        logger.info(f"현재 시각: {current_time_str} | 발송 시간: {term_time} => 운세 메시지가 생성될 시간입니다." )
    else:
        logger.info(f"현재 시각: {current_time_str} | 발송 시간: {term_time} => 운세 메시지가 생성될 시간이 아닙니다." )
        return