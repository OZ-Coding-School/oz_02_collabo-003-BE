from .views import *
import logging
import time

# 로깅 기본 설정: 로그 레벨, 로그 포맷, 파일 이름 등을 지정할 수 있습니다.
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename='gpt_jobs.log')

def gpt_today_job():
    request = None  # 필요한 경우 실제 request 객체를 제공해야 할 수도 있다.
    
    try:
        GptToday().post(request)
        logging.info("GptToday 작업이 성공적으로 실행되었습니다. (기존 데이터가 있다가면 추가되지 않았습니다.)")
    except Exception as e:
        logging.error(f"Error occurred during GptToday job execution: {e}")
        return    # 현재 함수 실행을 중지합니다.
    time.sleep(60) # 1분 대기

    try:
        GptStar().post(request)
        logging.info("GptStar 작업이 성공적으로 실행되었습니다. (기존 데이터가 있다가면 추가되지 않았습니다.)")
    except Exception as e:
        logging.error(f"Error occurred during GptToday job execution: {e}")
        return 
    time.sleep(120) # 2분 대기

    try:
        GptMbti().post(request)
        logging.info("GptMbti 작업이 성공적으로 실행되었습니다. (기존 데이터가 있다가면 추가되지 않았습니다.)")
    except Exception as e:
        logging.error(f"Error occurred during GptToday job execution: {e}")
        return 
    time.sleep(120) # 2분 대기

    try:
        GptZodiac().post(request)
        logging.info("GptZodiac 작업이 성공적으로 실행되었습니다. (기존 데이터가 있다가면 추가되지 않았습니다.)")
    except Exception as e:
        logging.error(f"Error occurred during GptToday job execution: {e}")
        return
