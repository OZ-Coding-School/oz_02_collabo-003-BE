from django.shortcuts import render
from datetime import datetime
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import PromptEachSerializer, PromptUpdateSerializer, PromptAllSerializer
from .models import GptPrompt

# Create your views here.
class GptPromptEach(APIView):
    serializer_class = PromptEachSerializer
    def get(self, request):
        try:
            # 카테고리별 가장 마지막 gpt_id 보여주기
            pass
        except:
            pass


class GptPromptUpdate(APIView):
    pass

class GptPromptAll(APIView):
    pass
