import firebase_admin # Firebase Admin SDK 사용
from firebase_admin import credentials # 서비스 계정 키를 사용하여 Firebase Admin SDK 인증
from firebase_admin import messaging # FCM 메시지 생성 및 전송
from django.utils import timezone
from datetime import datetime, timedelta
from .models import DeviceToken
from luck_messages.models import LuckMessage
import logging

# 푸시 알림 로그 따로 쌓기
# logger instence 생성
push_logger = logging.getLogger('push_jobs')
# log level 설정
push_logger.setLevel(logging.INFO)
# 파일 핸들러 생성
file_handler = logging.FileHandler('push_jobs.log')
push_logger.addHandler(file_handler)
# 포맷 설정
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(funcName)s:%(lineno)s - %(message)s')
file_handler.setFormatter(formatter)

# push 보내는 함수
def send_push_notifications():
    # firebase adminsdk 초기화
    cred_path = 'kluck_notifications/kluck-firebase.json'
    try:
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred) # 초기화 한번만
        push_logger.info("Firebase Admin SDK 초기화 성공")
    except Exception as e:
        push_logger.error(f"Firebase Admin SDK 초기화 실패: {e}")
        return


    try:
        # DB에서 디바이스 토큰 가져오기
        registration_tokens = list(DeviceToken.objects.values_list('token', flat=True))

        # 오늘 날짜 가져오기
        today = datetime.now().strftime("%Y%m%d")
        # DB에서 오늘의 운세 메시지 가져오기
        today_luck_msg = LuckMessage.objects.filter(luck_date=today, category='today').first()

        # 오늘의 운세 메시지가 존재한다면 푸시 알림 보내기
        if today_luck_msg:
            title = '오늘의 운세'
            body = today_luck_msg.luck_msg
            
            # 푸시 알림 메시지 생성
            message = messaging.MulticastMessage( # 여러 기기에 메시지 전송
                notification=messaging.Notification(
                    title=title,
                    body=body,
                ),
                # Android 알림 설정
                android=messaging.AndroidConfig(
                    # 알림 유효 시간 == 1시간 (알림 유지)
                    ttl=timedelta(seconds=3600),
                    # 알림 우선 순위 == 일반
                    priority='normal',
                    # 알림 아이콘 설정
                    notification=messaging.AndroidNotification(
                        icon='https://exodus-web.gcdn.ntruss.com/static/appicon_512_512.png',
                        sound='default',
                        # click_action='FLUTTER_NOTIFICATION_CLICK',
                    )
                ),
                tokens = registration_tokens, # 여러 개의 등록 토큰 리스트
            )

            # Firebase로 푸시 알림 전송
            response = messaging.send_multicast(message)
            push_logger.info(f"푸시 알림 발송 성공. Response: {response}")
        else:
            push_logger.info(f"오늘의 운세 메시지가 존재하지 않습니다. today_luck_msg: {today_luck_msg}")
            
    except Exception as e:
        push_logger.error(f"푸시 알림 전송 중 오류 발생: {e}")

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
