from datetime import datetime
from rest_framework import views, status
from rest_framework.response import Response
from .serializers import *


class findTodayZodiacMessages(views.APIView):
    serializer_class = zodiacSerializer
    def get(self, request, attribute1):
        now = datetime.now()
        date = now.strftime("%Y%m%d")
        reqCategory = "zodiac"
        messages = LuckMessage.objects.filter(luck_date=date, category=reqCategory, attribute1=attribute1)
        serializer = zodiacSerializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

