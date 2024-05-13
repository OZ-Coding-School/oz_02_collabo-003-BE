from datetime import datetime
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
import random
from .models import LuckMessage
from drf_spectacular.utils import extend_schema


# api/v1/msg/main/
class TodayLuck(APIView):
    '''
        BE-LUCK101(202, 302, 402): 사용자 정보에 맞는 오늘날짜의 한마디, 띠, 별, MBTI 운세 로드
    '''
    # 오늘 날짜의 Today, 띠, 별, MBTI 메세지 조회
    serializer_class = TodayLuckSerializer

    @extend_schema(tags=['Msg'])
    def get(self, request, user_birth, user_MBTI):
        try:
            # 오늘 날짜 가져오기, 입력 받은 사용자의 데이터를 변수로 저장.
            now = datetime.now()
            today = now.strftime("%Y%m%d")
            # user_birth = request.GET.get('user_birth')
            # user_MBTI = request.GET.get('user_MBTI')

            # 오늘의 한마디 사용자에게 제공.
            # 3가지의 오늘의 한마디에서 랜덤하게 제공.

            today_msg = LuckMessage.objects.filter(luck_date=today, attribute2=random.randint(0,4))
            if today_msg:
                today_serializer = TodayLuckSerializer(today_msg[0]).data
            else:
                today_serializer = {}

            ran_num = random.randint(0, 4)
            today_msg = LuckMessage.objects.filter(luck_date=today, attribute2=ran_num)


            # 사용자 출생연도에 맞는 띠별 오늘의 운세 제공.
            user_zodiac = user_birth[:4]
            zodiac_msg = LuckMessage.objects.filter(luck_date=today, attribute2=user_zodiac)
            if zodiac_msg:
                zodiac_serializer = TodayLuckSerializer(zodiac_msg[0]).data
            else:
                zodiac_serializer = {}

            # 사용자 출생월일에 맞는 별자리별 오늘의 운세 제공.
            user_star = int(user_birth[4:])
            if user_star >= 120 and user_star <= 218:
                star = "물병자리"
            elif user_star >= 219 and user_star <= 320:
                star = "물고기자리"
            elif user_star >= 321 and user_star <= 419:
                star = "양자리"
            elif user_star >= 420 and user_star <= 520:
                star = "황소자리"
            elif user_star >= 521 and user_star <= 620:
                star = "쌍둥이자리"
            elif user_star >= 621 and user_star <= 722:
                star = "게자리"
            elif user_star >= 723 and user_star <= 822:
                star = "사자자리"
            elif user_star >= 823 and user_star <= 922:
                star = "처녀자리"
            elif user_star >= 923 and user_star <= 1022:
                star = "천칭자리"
            elif user_star >= 1023 and user_star <= 1121:
                star = "전갈자리"
            elif user_star >= 1122 and user_star <= 1221:
                star = "궁수자리"
            else:
                star = "염소자리"
            star_msg = LuckMessage.objects.filter(luck_date=today, attribute1=star)
            star_serializer = TodayLuckSerializer(star_msg[0]).data

            # 사용자 MBTI에 맞는 MBTI별 오늘의 운세 제공.
            mbti_msg = LuckMessage.objects.filter(luck_date=today, attribute1=user_MBTI)
            if mbti_msg:
                mbti_serializer = TodayLuckSerializer(mbti_msg[0]).data
            else:
                mbti_serializer = {}

            serializer = {
                'today_msg': today_serializer,
                'zodiac_msg': zodiac_serializer,
                'star_msg': star_serializer,
                'mbti_msg': mbti_serializer
            }

            return Response(serializer, status=status.HTTP_200_OK)

        except LuckMessage.DoesNotExist:
            raise Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
            
            
#api/v1/msg/zodiac_all/{띠이름}
class FindTodayZodiacMessages(APIView):
    '''
        BE-LUCK201: 오늘날짜의 띠 메세지 로드
    '''
    serializer_class = ZodiacSerializer

    @extend_schema(tags=['Msg'])
    def get(self, request, attribute1):
        now = datetime.now()
        date = now.strftime("%Y%m%d")
        reqCategory = "zodiac"
        messages = LuckMessage.objects.filter(luck_date=date, category=reqCategory, attribute1=attribute1)
        serializer = ZodiacSerializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


#api/v1/msg/star_all
class FindTodayStarMessages(APIView):
    '''
        BE-LUCK301: 오늘날짜의 별자리 메세지 로드
    '''
    serializer_class = StarSerializer

    @extend_schema(tags=['Msg'])
    def get(self, request):
        now = datetime.now()
        date = now.strftime("%Y%m%d")
        reqCategory = "star"
        messages = LuckMessage.objects.filter(luck_date=date, category=reqCategory)
        serializer = StarSerializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


#api/v1/msg/mbti_all
class FindTodayMbtiMessages(APIView):
    '''
        BE-LUCK401: 오늘날짜의 MBTI 메세지 로드
    '''
    serializer_class = MbtiSerializer

    @extend_schema(tags=['Msg'])
    def get(self, request):
        now = datetime.now()
        date = now.strftime("%Y%m%d")
        reqCategory = 'mbti'
        messages = LuckMessage.objects.filter(luck_date=date, category=reqCategory)
        serializer = MbtiSerializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)









#/api/v1/msg/today/<str:luck_date>
class FindSomedayTodayMessages(APIView):
    '''
        BE-GPT104: 특정 날짜별 한마디 메세지 로드
    '''
    serializer_class = TodaySerializer

    @extend_schema(tags=['AdminMsg'])
    def get(self, request, luck_date):
        reqCategory = "today"
        messages = LuckMessage.objects.filter(luck_date=luck_date, category=reqCategory)
        serializer = TodaySerializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


#/api/v1/msg/zodiac/<str:luck_date>
class FindSomedayZodiacMessages(APIView):
    '''
        BE-GPT204: 특정 날짜별 띠 메세지 로드
    '''
    serializer_class = ZodiacSerializer

    @extend_schema(tags=['AdminMsg'])
    def get(self, request, luck_date):
        reqCategory = "zodiac"
        messages = LuckMessage.objects.filter(luck_date=luck_date, category=reqCategory)
        serializer = ZodiacSerializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


#/api/v1/admin/star/<str:luck_date>
class FindSomedayStarMessages(APIView):
    '''
        BE-GPT304: 특정 날짜별 별자리 메세지 로드
    '''
    serializer_class = StarSerializer

    @extend_schema(tags=['AdminMsg'])
    def get(self, request, luck_date):
        reqCategory = "star"
        messages = LuckMessage.objects.filter(luck_date=luck_date, category=reqCategory)
        serializer = StarSerializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


#/api/v1/admin/mbti/<str:luck_date>
class FindSomedayMbtiMessages(APIView):
    '''
    BE-GPT404: 특정 날짜별 MBTI 메세지 로드
    '''
    serializer_class = MbtiSerializer

    @extend_schema(tags=['AdminMsg'])
    def get(self, request, luck_date):
        reqCategory = 'mbti'
        messages = LuckMessage.objects.filter(luck_date=luck_date, category=reqCategory)
        serializer = MbtiSerializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
