from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema
from django.shortcuts import get_object_or_404
from admin_settings.models import AdminSetting
from .serializers import *
from .models import LuckMessage
from operator import itemgetter
from datetime import datetime, timedelta
import re
# import random

# urls.py
# api/v1/msg/main/
class TodayLuck(APIView):
    '''
        BE-LUCK101(202, 302, 402): 사용자 정보에 맞는 오늘날짜의 한마디, 띠, 별, MBTI 운세 로드
    '''
    # 오늘 날짜의 Today, 띠, 별, MBTI 메세지 조회
    serializer_class = TodayLuckSerializer
    permission_classes = (AllowAny,)

    @extend_schema(tags=['Msg'])
    def get(self, request, user_birth, user_MBTI):
        try:
            # 오늘 날짜 가져오기, 입력 받은 사용자의 데이터를 변수로 저장.
            now = datetime.now()
            today = now.strftime("%Y%m%d")

            # 오늘의 한마디 사용자에게 제공.
            # 3가지의 오늘의 한마디에서 랜덤하게 제공.
            # ran_num = random.randint(1,3)

            today_msg = LuckMessage.objects.filter(luck_date=today, category='today')
            if today_msg:
                today_serializer = TodayLuckSerializer(today_msg[0]).data
            else:
                today_serializer = {'새벽 공기처럼 맑고 상쾌한 기운이 가득하길.🍃✨ 마음 가득 행복이 채워지는 날 되세요.🌷'}


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
            elif user_star >= 521 and user_star <= 621:
                star = "쌍둥이자리"
            elif user_star >= 622 and user_star <= 722:
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
    permission_classes = (AllowAny,)

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
    permission_classes = (AllowAny,)

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
    permission_classes = (AllowAny,)

    @extend_schema(tags=['Msg'])
    def get(self, request):
        now = datetime.now()
        date = now.strftime("%Y%m%d")
        reqCategory = 'mbti'
        messages = LuckMessage.objects.filter(luck_date=date, category=reqCategory)
        serializer = MbtiSerializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


######################
# urls_admin.py

#/api/v1/admin/today/<str:luck_date>
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


#/api/v1/admin/zodiac/<str:luck_date>
class FindSomedayZodiacMessages(APIView):
    '''
        BE-GPT204: 특정 날짜별 띠 메세지 로드
    '''
    serializer_class = ZodiacSerializer

    @extend_schema(tags=['AdminMsg'])
    def get(self, request, luck_date):
        reqCategory = "zodiac"
        messages = LuckMessage.objects.filter(luck_date=luck_date, category=reqCategory)

        # 데이터를 attribute1로 그룹화하고 attribute2 기준 오름차순 정렬
        result = []
        for message in messages:
            attribute1 = message.attribute1
            message_dict = next((item for item in result if item["attribute1"] == attribute1), None)
            if message_dict:
                message_dict["messages"].append({
                    "msg_id": message.msg_id, # msg_id
                    "attribute2": message.attribute2,
                    "luck_msg": message.luck_msg
                })
            else:
                result.append({
                    "attribute1": attribute1,
                    "messages": [{
                        "msg_id": message.msg_id,
                        "attribute2": message.attribute2,
                        "luck_msg": message.luck_msg
                    }]
                })
        
        for item in result:
            item["messages"] = sorted(item["messages"], key=itemgetter("attribute2"))
        
        return Response(result, status=status.HTTP_200_OK)


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


# /api/v1/admin/dashboard/
class AdminDashboard(APIView):
    '''
    BE-ADM010: 관리자 페이지 메인 화면 [콘텐츠 생성 현황]과 관련된 스케줄러 작동 현황 데이터 보내기.
    '''
    # 오늘 날짜 스케줄러에서 생성한 메시지 상태 확인
    serializer = TodayLuckSerializer
    
    @extend_schema(tags=['AdminMsg'])
    def get(self, request):
        now = datetime.now()
        term = get_object_or_404(AdminSetting).term_date
        date = now + timedelta(days=int(term))
        scheduler_date = date.strftime('%Y%m%d')
        today_scheduler = LuckMessage.objects.filter(category='work', luck_date=scheduler_date)

        if not today_scheduler.exists():
            return Response(f"{scheduler_date} 생성 오류", status=status.HTTP_404_NOT_FOUND)
        else:
            scheduler_status = LuckMessage.objects.filter(category='work', luck_date=scheduler_date, attribute2=0)
            if scheduler_status.exists():
                return Response(f"{scheduler_date} 생성 중", status=status.HTTP_226_IM_USED)
            else:
                success_counts = [get_success_count(item.luck_msg) for item in today_scheduler]
                if all(count == 31 for count in success_counts):
                    return Response(f"{scheduler_date} 생성 완료", status=status.HTTP_200_OK)
                elif any(count == 0 for count in success_counts):
                    return Response(f"{scheduler_date} 생성 완료", status=status.HTTP_200_OK)
                else:
                    return Response(f"{scheduler_date} 일부 생성 완료", status=status.HTTP_206_PARTIAL_CONTENT)


# luck_msg 필드 파싱 함수
def get_success_count(luck_msg):
    pattern = r'Success count = (\d+)'
    match = re.search(pattern, luck_msg)
    if match:
        return int(match.group(1))
    else:
        return None


#/api/v1/admin/luckdays
class LuckDays(APIView):
    # 오늘 날짜 확인
    # 4가지 카테고리의 오늘포함 오늘보다 큰 날짜 값 조회 및 리스트로 저장
    # 4가지 카테고리의 날짜값을 비교해서 모두 중복되는 날짜만 남기는 리스트 저장 및 반환
    serializer_class = LuckMessagesSerializer

    @extend_schema(tags=['AdminMsg'])
    def get(self, request):
        now = datetime.now()
        date = now.strftime("%Y%m%d")
        # 4가지 카테고리의 오늘포함 오늘보다 큰 날짜 값 조회 및 리스트로 저장
        # 카테고리 조회
        categories_QuerySet = LuckMessage.objects.values_list('category', flat=True).distinct()
        categories_dict = {
            'today' : [],
            'star' : [],
            'MBTI' : [],
            'zodiac' : []
        }
        # 카테고리별 반복, work, None 제외
        for category in categories_QuerySet:
            if category in ['work', None]:
                continue
            if category in categories_dict:
                luck_dates = LuckMessage.objects.filter(category=category, luck_date__gte=date).order_by('luck_date')
                serializer = LuckMessagesSerializer(luck_dates, many=True, fields=('luck_date',))
                # 카테고리명으로 각각의 날짜값 저장
                for luck_date in serializer.data:
                    categories_dict[category].append(luck_date["luck_date"])
                categories_dict[category] = list(set(categories_dict[category]))
        # 카테고리중에서 가장 많은 날짜 개수 파악
        # 카테고리별 운세 수를 저장할 딕셔너리 선언
        luck_date_cnt = {}
        # 카테고리별 운세 수 저장
        for category in categories_dict:
            luck_date_cnt[category] = (len(categories_dict[category]))
        # 카테고리 운세 수 중에서 가장 작은 카테고리 선택 모두 같은 경우 today선택
        # 카테고리별 숫자 비교용 리스트 선언
        category_cnt = []
        for key, value in luck_date_cnt.items():
            category_cnt.append(value)

        # 날짜의 숫자가 다른 날이 있는지 파악
        # 카테고리별 운세가 있는 날짜 수 확인
        category_cnt = set(category_cnt)
        # 조회 대상 카테고리 변수 선언
        target_category = ''
        # 운세 수가 서로 다른 카테고리가 있다면 그중에 수가 가장 작은 카테고리 선택
        if len(category_cnt) != 1:
            for key, value in luck_date_cnt.items():
                # 가장 작은 숫자가 여럿이라면 가장 마지막 카테고리가 선택됨
                if value == min(category_cnt):
                    target_category = key
        else:
            # 운세 수가 모두 같다면 가장 첫번째 카테고리 선택
            target_category = next(iter(luck_date_cnt),None)

        # 선택된 카테고리 여부 판단
        if target_category == None:
            luck_days = {'luck_days':""}
        else:
            categories_dict[target_category].sort()
            luck_days = {'luck_days':categories_dict[target_category]}

        return Response(luck_days, status=status.HTTP_200_OK)
