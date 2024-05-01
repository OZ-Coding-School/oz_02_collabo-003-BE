from datetime import datetime
from rest_framework import views, status
from rest_framework.response import Response
from .serializers import *

class findSomedayZodiacMessages(views.APIView):
    serializer_class = zodiacSerializer
    def get(self, request, luck_date):
        reqCategory = "zodiac"
        messages = LuckMessage.objects.filter(luck_date=luck_date, category=reqCategory)
        serializer = zodiacSerializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
