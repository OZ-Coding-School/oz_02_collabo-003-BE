from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from .models import *
from.serializers import *

# push 알림을 위한 토큰 받아오기
class PushToken(APIView):
    @extend_schema(tags=['PushToken'])
    def post(self, request):
        serializer = DeviceTokenSerializer(data=request.data)

        if serializer.is_valid():
            token = serializer.validated_data['token']
            app_name = serializer.validated_data['app_name']

            token_exists = DeviceToken.objects.filter(token=token, app_name=app_name).exists()

            if not token_exists:
                serializer.save()
                return Response({'message': '토큰이 저장되었습니다.'}, status=status.HTTP_201_CREATED)
            else: 
                return Response({'message': '토큰이 이미 존재합니다.'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)