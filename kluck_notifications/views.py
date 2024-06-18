from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema, OpenApiExample
from django.utils import timezone
from .models import *
from.serializers import *

import logging

# 푸시 로거 가져오기
push_logger = logging.getLogger('push_jobs')


# push 알림을 위한 토큰 받아오기
class PushToken(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = () 
    serializer_class = DeviceTokenSerializer
    
    # 스웨거 UI
    @extend_schema(tags=['PushToken'],
        examples=[
            OpenApiExample(
                'Example',
                value={'token': 'abcd1234efgh5678', 'device_os': 'android'},
                request_only=True,  # 요청 본문에서만 예시 사용
            )
        ],
        description="Device Token"
    )
    
    def post(self, request):
        push_logger.info(f"PushToken API에 POST 요청이 들어왔습니다. data: {request.data}")
        serializer = DeviceTokenSerializer(data=request.data)

        if serializer.is_valid(): # 유효한 데이터일 경우, 데이터 추출
            token = serializer.validated_data['token']
            device_os = serializer.validated_data['device_os']

            # 중복 토큰 검사
            token_exists = DeviceToken.objects.filter(token=token, device_os=device_os).first()

            if not token_exists: # 토큰이 중복되지 않는 경우, 토큰 저장
                serializer.save()
                push_logger.info(f"새로운 토큰이 저장되었습니다: {token}")
                return Response({'message': '토큰이 저장되었습니다.'}, status=status.HTTP_201_CREATED)
            else: # 토큰이 중복되는 경우, update_date 갱신
                token_exists.update_date = timezone.now()
                token_exists.save()
                push_logger.info(f"기존 토큰이 갱신되었습니다: {token}")
                return Response({'message': '토큰이 갱신되었습니다.'}, status=status.HTTP_200_OK)
        else:
            push_logger.error(f"유효하지 않은 데이터가 POST 요청에서 받아졌습니다. error: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
