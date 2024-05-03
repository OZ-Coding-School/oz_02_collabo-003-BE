from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from datetime import datetime, timedelta
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from .models import GptPrompt

# Create your views here.

# 오늘의 한마디 프롬프트
# api/v1/prompt/today
class PromptToday(APIView):
    # 프롬프트 최신 메세지 로드 - 가장 마지막 gpt_id 보여주기
    serializer_class = PromptTodaySerializer
    def get(self, request):
        # 업데이트하는 방식 X, 프롬프트 메세지 이름 사용 X
        try:
            category = "today"
            latest_today = GptPrompt.objects.filter(category=category).order_by('-gpt_id').first()
            serializer = PromptTodaySerializer(latest_today)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except GptPrompt.DoesNotExist:
            return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

    # 프롬프트 메세지 수정 - 추가하는 방식
    def post(self, request):
        now = datetime.now()
        today = now.strftime('%Y%m%d')
        admins_id = 1
        serializer = PromptTodaySerializer(data=request.data, context={'admins_id': admins_id})

        if serializer.is_valid():
            category = 'today'
            prompt_msg_name = today
            create_date = today
            last = now + timedelta(days=7)
            last_date = last.strftime('%Y%m%d')

            serializer.save(category=category, prompt_msg_name=prompt_msg_name,
                            create_date=create_date, last_date=last_date, admins_id=admins_id)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

# 띠별 운세 프롬프트
# api/v1/prompt/zodiac
class PromptZodiac(APIView):
    # 프롬프트 최신 메세지 로드 - 가장 마지막 gpt_id 보여주기
    serializer_class = PromptZodiacSerializer
    def get(self, request):
    # 업데이트하는 방식 X, 프롬프트 메세지 이름 사용 X
        try:
            category = "zodiac"
            latest_zodiac = GptPrompt.objects.filter(category=category).order_by('-gpt_id').first()
            serializer = PromptZodiacSerializer(latest_zodiac)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except GptPrompt.DoesNotExist:
            return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

    # 프롬프트 메세지 수정 - 추가하는 방식
    def post(self, request):
        now = datetime.now()
        today = now.strftime('%Y%m%d')
        admins_id = 1
        serializer = PromptZodiacSerializer(data=request.data, context={'admins_id': admins_id})

        if serializer.is_valid():
            category = 'zodiac'
            prompt_msg_name = today
            create_date = today
            last = now + timedelta(days=7)
            last_date = last.strftime('%Y%m%d')

            serializer.save(category=category, prompt_msg_name=prompt_msg_name,
                            create_date=create_date, last_date=last_date, admins_id=admins_id)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)


# 별자리별 운세 프롬프트
# api/v1/prompt/star
class PromptStar(APIView):
    # 프롬프트 최신 메세지 로드 - 가장 마지막 gpt_id 보여주기
    serializer_class = PromptStarSerializer
    def get(self, request):
        # 업데이트하는 방식 X, 프롬프트 메세지 이름 사용 X
        # api/v1/prompt/star
        try:
            category = "star"
            latest_star = GptPrompt.objects.filter(category=category).order_by('-gpt_id').first()
            serializer = PromptStarSerializer(latest_star)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except GptPrompt.DoesNotExist:
            return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

    # 프롬프트 메세지 수정 - 추가하는 방식
    def post(self, request):
        now = datetime.now()
        today = now.strftime('%Y%m%d')
        admins_id = 1
        serializer = PromptStarSerializer(data=request.data, context={'admins_id': admins_id})

        if serializer.is_valid():
            category ='star'
            prompt_msg_name = today
            create_date = today
            last = now + timedelta(days=7)
            last_date = last.strftime('%Y%m%d')

            serializer.save(category=category, prompt_msg_name=prompt_msg_name,
                            create_date=create_date, last_date=last_date, admins_id=admins_id)
            return Response(serializer.data, status=status.HTTP_200_OK)


# MBTI별 운세 프롬프트
# api/v1/prompt/mbti
class PromptMbti(APIView):
    # 프롬프트 최신 메세지 로드 - 가장 마지막 gpt_id 보여주기
    serializer_class = PromptMbtiSerializer
    def get(self, request):
        # 업데이트하는 방식 X, 프롬프트 메세지 이름 사용 X
        try:
            category = "mbti"
            latest_mbti = GptPrompt.objects.filter(category=category).order_by('-gpt_id').first()
            serializer = PromptMbtiSerializer(latest_mbti)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except GptPrompt.DoesNotExist:
            return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

    # 프롬프트 메세지 수정 - 추가하는 방식
    def post(self, request):
        now = datetime.now()
        today = now.strftime('%Y%m%d')
        admins_id = 1
        serializer = PromptMbtiSerializer(data=request.data, context={'admins_id': admins_id})

        if serializer.is_valid():
            category ='MBTI'
            prompt_msg_name = today
            create_date = today
            last = now + timedelta(days=7)
            last_date = last.strftime('%Y%m%d')

            serializer.save(category=category, prompt_msg_name=prompt_msg_name,
                            create_date=create_date, last_date=last_date, admins_id=admins_id)
            return Response(serializer.data, status=status.HTTP_200_OK)


# 카테고리별 프롬프트 메세지 전체 로드
class PromptHistory(APIView):
    # api/v1/prompt/<str:category>/history
    serializer_class = PromptHistorySerializer
    def get(self, request, category):
        try:
            prompt_msgs = GptPrompt.objects.filter(category=category)
            serializer = self.get_serializer(prompt_msgs, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except GptPrompt.DoesNotExist:
            return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)