from rest_framework import views, status
from rest_framework.response import Response
from .serializers import *
from luck_messages.models import LuckMessage

class TodayMessage(views.APIView):
    serializer_class = TodaySerializer
    def post(self, request, msg_id):
        try:
            msg_id = LuckMessage.objects.get(pk=msg_id)
        except LuckMessage.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = TodaySerializer(msg_id, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)