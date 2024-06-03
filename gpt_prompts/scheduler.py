import logging
import time
from django.core.mail import send_mail
from django.conf import settings
from .views import *

# 로깅 기본 설정: 로그 레벨, 로그 포맷, 파일 이름 등을 지정할 수 있습니다.
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename='gpt_jobs.log')

# 이메일 전송 함수
def send_email(subject, message, recipient_list):
    try:
        # 지정된 백엔드를 사용하여 이메일을 보내는 Django 함수
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=recipient_list,
            fail_silently=False,
        )
        logging.info(f"이메일이 성공적으로 전송되었습니다. 수신자: {recipient_list}, 제목: {subject}")
        print("Email send successfully")
    except Exception as e:
        logging.info(f"이메일 전송 중 오류가 발생했습니다: {e}")
        print(f"Email send failed: {e}")

# 주요 작업 함수
def gpt_today_job():
    request = None  # 필요한 경우 실제 request 객체를 제공해야 할 수도 있다.
    success_count = 0
    
    try:
        GptToday().post(request)
        logging.info("GptToday 작업이 성공적으로 실행되었습니다. (기존 데이터가 있다가면 추가되지 않았습니다.)")
        success_count += 1
    except Exception as e:
        logging.error(f"Error occurred during GptToday job execution: {e}")
        return    # 현재 함수 실행을 중지합니다.
    time.sleep(60) # 1분 대기

    try:
        GptStar().post(request)
        logging.info("GptStar 작업이 성공적으로 실행되었습니다. (기존 데이터가 있다가면 추가되지 않았습니다.)")
        success_count += 1
    except Exception as e:
        logging.error(f"Error occurred during GptStar job execution: {e}")
        return 
    time.sleep(120) # 2분 대기

    try:
        GptMbti().post(request)
        logging.info("GptMbti 작업이 성공적으로 실행되었습니다. (기존 데이터가 있다가면 추가되지 않았습니다.)")
        success_count += 1
    except Exception as e:
        logging.error(f"Error occurred during GptMbti job execution: {e}")
        return 
    time.sleep(120) # 2분 대기

    try:
        GptZodiac().post(request)
        logging.info("GptZodiac 1차 작업이 성공적으로 실행되었습니다. (기존 데이터가 있다가면 추가되지 않았습니다.)")
        success_count += 1
    except Exception as e:
        logging.error(f"Error occurred during GptZodiac job execution: {e}")
        return
    
    return success_count

result = gpt_today_job()
print(result)

if result == 4:
    subject="Scheduler Success"
    message="Scheduler 동작이 정상적으로 실행되었습니다."
else:
    subject="Scheduler Fail"
    message="Scheduler 동작 중 오류가 발생했습니다."
    
recipient_list=["j00whii@gmail.com"]

send_email(subject, message, recipient_list)
