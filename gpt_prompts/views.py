from django.shortcuts import render
from datetime import datetime, timedelta
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from .serializers import *
from .models import GptPrompt

# Create your views here.

# 오늘의 한마디 프롬프트
class PromptToday(APIView):
    # 프롬프트 최신 메세지 로드 - 가장 마지막 gpt_id 보여주기
    # api/v1/prompt/today/
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

class PromptHistory(GenericAPIView):
    # 프롬프트 메세지 전체 로드
    # api/v1/prompt/<str:category>/history
    serializer_class = PromptHistorySerializer
    def get(self, request, category):
        try:
            prompt_msgs = GptPrompt.objects.filter(category=category)
            serializer = self.get_serializer(prompt_msgs, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except GptPrompt.DoesNotExist:
            return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)


# # 띠별 운세 프롬프트
# class PromptZodiac(APIView):
#     # 프롬프트 최신 메세지 로드 - 가장 마지막 gpt_id 보여주기
#     def get(self, request):
#         # 업데이트하는 방식 X, 프롬프트 메세지 이름 사용 X
#         try:
#             pass
#         except:
#             pass

#     # 프롬프트 메세지 수정 - 추가하는 방식
#     def post(self, request, prompt_msg, admins_id):
#         try:
#             pass
#         except:
#             pass


# # 별자리별 운세 프롬프트
# class PromptStar(APIView):
#     # 프롬프트 최신 메세지 로드 - 가장 마지막 gpt_id 보여주기
#     def get(self, request):
#         # 업데이트하는 방식 X, 프롬프트 메세지 이름 사용 X
#         try:
#             pass
#         except:
#             pass

#     # 프롬프트 메세지 수정 - 추가하는 방식
#     def post(self, request, prompt_msg, admins_id):
#         try:
#             pass
#         except:
#             pass


# # MBTI별 운세 프롬프트
# class PromptMbti(APIView):
#     # 프롬프트 최신 메세지 로드 - 가장 마지막 gpt_id 보여주기
#     def get(self, request):
#         # 업데이트하는 방식 X, 프롬프트 메세지 이름 사용 X
#         try:
#             pass
#         except:
#             pass

#     # 프롬프트 메세지 수정 - 추가하는 방식
#     def post(self, request, prompt_msg, admins_id):
#         try:
#             pass
#         except:
#             pass
