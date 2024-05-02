from django.http import HttpResponse
from datetime import datetime
import random
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import TodayLuckSerializer
from .models import LuckMessage

# Create your views here.
# api/v1/main/
class TodayLuck(APIView):
    def get(self, request, user_birth, user_MBTI):
        try:
            # 오늘 날짜 가져오기, 입력 받은 사용자의 데이터를 변수로 저장.
            now = datetime.now()
            today = now.strftime("%Y%m%d")
            # user_birth = request.GET.get('user_birth')
            # user_MBTI = request.GET.get('user_MBTI')

            # 오늘의 한마디 사용자에게 제공.
            # 3가지의 오늘의 한마디에서 랜덤하게 제공.
            ran_num = random.randint(0,4)
            today_msg = LuckMessage.objects.filter(luck_date=today, attribute2=ran_num)

            # 사용자 출생연도에 맞는 띠별 오늘의 운세 제공.
            user_zodiac = user_birth[:4]
            zodiac_msg = LuckMessage.objects.filter(luck_date=today, attribute2=user_zodiac)

            # 사용자 출생월일에 맞는 별자리별 오늘의 운세 제공.
            user_star = int(user_birth[4:])
            if user_star>=120 and user_star<=218:
                star="물병자리"
            elif user_star>=219 and user_star<=320:
                star="물고기자리"
            elif user_star>=321 and user_star<=419:
                star="양자리"
            elif user_star>=420 and user_star<=520:
                star="황소자리"
            elif user_star>=521 and user_star<=620:
                star="쌍둥이자리"
            elif user_star>=621 and user_star<=722:
                star="게자리"
            elif user_star>=723 and user_star<=822:
                star="사자자리"
            elif user_star>=823 and user_star<=922:
                star="처녀자리"
            elif user_star>=923 and user_star<=1022:
                star="천칭자리"
            elif user_star>=1023 and user_star<=1121:
                star="전갈자리"
            elif user_star>=1122 and user_star<=1221:
                star="궁수자리"
            else:
                star="염소자리"
            star_msg = LuckMessage.objects.filter(luck_date=today, attribute1=star)

            # 사용자 MBTI에 맞는 MBTI별 오늘의 운세 제공.
            mbti_msg = LuckMessage.objects.filter(luck_date=today, attribute1=user_MBTI)

            today_serializer = TodayLuckSerializer(today_msg[0]).data
            zodiac_serializer = TodayLuckSerializer(zodiac_msg[0]).data
            star_serializer = TodayLuckSerializer(star_msg[0]).data
            mbti_serializer = TodayLuckSerializer(mbti_msg[0]).data

            serializer = {
                'today_msg' : today_serializer,
                'zodiac_msg' : zodiac_serializer,
                'star_msg' : star_serializer,
                'mbti_msg' : mbti_serializer
            }
            
            return Response(serializer, status=status.HTTP_200_OK)

        except LuckMessage.DoesNotExist:
            raise Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

