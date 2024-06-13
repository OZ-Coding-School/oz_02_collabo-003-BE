from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from .models import *

# push 알림을 위한 토큰 받아오기
class PushToken(APIView):
    @extend_schema(tags=['PushToken'])
    def post(self, request):
        # 토큰 데이터 가져오기
        token = request.data.get('token')
        # 어느 앱 토큰인지 식별하기 위함
        app_name = request.data.get('app_name')

        # 토큰이나 앱 이름이 존재하지 않을 경우
        if not token or not app_name:
            return Response({'message': '토큰 또는 앱 이름이 제공되지 않았습니다.'}, status=status.HTTP_400_BAD_REQUEST)
        
        token_exists = DeviceToken.objects.filter(token=token, app_name=app_name).exists()

        if not token_exists:
            DeviceToken.objects.create(token=token, app_name=app_name)
            return Response({'message': '토큰이 저장되었습니다.'}, status=status.HTTP_201_CREATED)
        else: 
            return Response({'message': '토큰이 이미 존재합니다.'}, status=status.HTTP_200_OK)
