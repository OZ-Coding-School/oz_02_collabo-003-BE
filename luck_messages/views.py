from datetime import datetime
from rest_framework import views, status
from rest_framework.response import Response
from .serializers import *


class findSomedayTodayMessages(views.APIView):
    serializer_class = todaySerializer
    def get(self, request, luck_date):
        reqCategory = "today"
        messages = LuckMessage.objects.filter(luck_date=luck_date, category=reqCategory)
        serializer = todaySerializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)