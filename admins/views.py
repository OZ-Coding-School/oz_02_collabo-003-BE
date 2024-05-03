from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from luck_messages.models import LuckMessage
from django.contrib.auth.password_validation import validate_password
from rest_framework.exceptions import ParseError
from django.contrib.auth.hashers import make_password


# api/v1/admin/signup/
class AdminUsers(APIView):
    serializer_class = AdminSignupSerializer
    def post(self, request):

        password = request.data.get('user_pw')
        serializer = AdminSignupSerializer(data=request.data)

        try:
            validate_password(password)
        except:
            raise ParseError('Password is invalid.')

        if serializer.is_valid():
            user = serializer.save()
            user.user_pw = make_password(password)
            user.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            raise ParseError(serializer.errors)


# api/v1/admin/msg/
class EditLuckMessage(APIView):
    '''
    프론트에서 msg_id를 받아 luck_messages의 모델에서 해당 id를 찾아 내용 수정
    수정 내용을 따로 다시 반환하지는 않는다.
    '''  
    serializer_class = LuckMessageSerializer
    def post(self, request):
        msg_id = request.data.get('msg_id')
        try:
            msg_id = LuckMessage.objects.get(msg_id=msg_id)
        except LuckMessage.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = LuckMessageSerializer(msg_id, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

