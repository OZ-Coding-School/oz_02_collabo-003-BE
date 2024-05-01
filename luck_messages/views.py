from datetime import datetime
from rest_framework import views, status
from rest_framework.response import Response
from .serializers import *


class findSomedayStarMessages(views.APIView):
    serializer_class = starSerializer
    def get(self, request, luck_date):
        reqCategory = "star"
        messages = LuckMessage.objects.filter(luck_date=luck_date, category=reqCategory)
        serializer = starSerializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
