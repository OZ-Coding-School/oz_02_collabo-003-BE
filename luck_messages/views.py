
from datetime import datetime
from rest_framework import views, status
from rest_framework.response import Response
from .serializers import *


class findTodayStarMessages(views.APIView):
    serializer_class = starSerializer
    def get(self, request):
        now = datetime.now()
        date = now.strftime("%Y%m%d")
        reqCategory = "star"
        messages = LuckMessage.objects.filter(luck_date=date, category=reqCategory)
        serializer = starSerializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
