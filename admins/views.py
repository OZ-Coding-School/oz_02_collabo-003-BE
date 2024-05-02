from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from luck_messages.models import LuckMessage

# api/v1/admin/zodiac/<int:msg_id>/update/
class ZodiacMessage(APIView):
    '''
    프론트에서 msg_id를 받아 luck_messages의 모델에서 해당 id를 찾아 내용 수정
    수정 내용을 따로 다시 반환하지는 않는다.
    '''  
    serializer_class = ZodiacSerializer
    def post(self, request, msg_id):
        try:
            msg_id = LuckMessage.objects.get(pk=msg_id)
        except LuckMessage.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ZodiacSerializer(msg_id, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# api/v1/admin/today/<int:msg_id>/update/
class TodayMessage(APIView):
    '''
    프론트에서 msg_id를 받아 luck_messages의 모델에서 해당 id를 찾아 내용 수정
    수정 내용을 따로 다시 반환하지는 않는다.
    '''
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