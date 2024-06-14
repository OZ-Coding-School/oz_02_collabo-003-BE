import firebase_admin # Firebase Admin SDK 사용
from firebase_admin import credentials # 서비스 계정 키를 사용하여 Firebase Admin SDK 인증
from firebase_admin import messaging # FCM 메시지 생성 및 전송
from kluck_env import env_settings as env
from datetime import datetime, timedelta
from .models import DeviceToken
from luck_messages.models import LuckMessage

# push 보내는 함수
def send_push_notifications():
    # firebase adminsdk 초기화
    cred_path = 'kluck_notifications/kluck-firebase.json'
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred) # 초기화 한번만

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
                        click_action='FLUTTER_NOTIFICATION_CLICK',
                    )
                ),
                tokens = registration_tokens, # 여러 개의 등록 토큰 리스트
            )
            print("푸시 알림 메시지 생성 완료")

            # Firebase로 푸시 알림 전송
            response = messaging.send_multicast(message)
            
    except Exception as e:
        print(f"푸시 알림 전송 중 오류 발생: {e}")
