from datetime import datetime
from rest_framework import views, status
from rest_framework.response import Response
from .serializers import *


class findSomedayMbtiMessages(views.APIView):
    serializer_class = mbtiSerializer
    def get(self, request, luck_date):
        reqCategory = 'mbti'
        messages = LuckMessage.objects.filter(luck_date=luck_date, category=reqCategory)
        serializer = mbtiSerializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

