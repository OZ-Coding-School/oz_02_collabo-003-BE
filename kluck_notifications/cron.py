from django.utils import timezone
from datetime import datetime, timedelta
from .push_scheduler import send_push_notifications
from .models import DeviceToken
from admin_settings.models import AdminSettings
import logging
import pytz

# 푸시 로거 가져오기
push_logger = logging.getLogger('push_jobs')

def push_cron_job():
    """
    매분마다 관리자 페이지에서 설정한 push_time과 현재 시각(한국 기준)을 비교한 후, 
    현재 시각이 push_time이면 푸시알림을 발송하고, push_time이 아니라면 푸시알림을 발송하지 않는다.
    """

    # DB에서 push_time 가져오기
    try:
        push_time = AdminSettings.objects.first().push_time
    except AttributeError:
        push_time = "0900" # 기본값 9시

    # 현재 시각
    current_time = datetime.now(pytz.timezone('Asia/Seoul'))
    # 현재 시각과 push_time 같은 형식으로 맞추기
    current_time_str = current_time.strftime('%H%M')

    # 현재 시각과 push_time이 같으면 푸시 발송
    if current_time_str == push_time:
        send_push_notifications()
        push_logger.info(f"현재 시각: {current_time_str} | 발송 시간: {push_time} => 푸시가 발송될 시간입니다." )
    else:
        push_logger.info(f"현재 시각: {current_time_str} | 발송 시간: {push_time} => 푸시가 발송될 시간이 아닙니다." )
        return

# 비활성화 토큰 삭제하기
def remove_inactive_tokens():
    try:
        # 비환성화 토큰 삭제 기준 날짜 (FCM 공식 문서 중 비활성 토큰 기간 참고 - 2개월)
        deactive_date = timezone.now() - timedelta(days=60)
        # 비활성화된 토큰 찾기 (update_date가 60일 초과했을 경우)
        inactive_tokens = DeviceToken.objects.filter(update_date__lt=deactive_date) # __lt : 작은 값 비교 / __lte : 작거나 같은 값
        # 비활성화 토큰 개수
        count = inactive_tokens.count()
        # 비활성화 토큰 삭제
        inactive_tokens.delete()
        
        # 삭제된 비활성화 토큰 개수 출력
        push_logger.info(f'Deleted {count} inactive tokens')

    except Exception as e:
        push_logger.error(f"비활성화 토큰 삭제 중 오류 발생: {e}")