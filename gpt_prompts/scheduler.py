from .views import *

def gpt_today_job():
    request = None  # 필요한 경우 실제 request 객체를 제공해야 할 수도 있다.
    GptToday().post(request)
    GptZodiac().post(request)
