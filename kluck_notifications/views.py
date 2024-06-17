from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiExample
from .models import *
from.serializers import *

# push 알림을 위한 토큰 받아오기
class PushToken(APIView):
    serializer_class = DeviceTokenSerializer
    
    # 스웨거 UI
    @extend_schema(tags=['PushToken'],
        examples=[
            OpenApiExample(
                'Example',
                value={'token': 'abcd1234efgh5678', 'device_os': 'Android'},
                request_only=True,  # 요청 본문에서만 예시 사용
            )
        ],
        description="Device Token"
    )
    
    def post(self, request):
        serializer = DeviceTokenSerializer(data=request.data)

        if serializer.is_valid(): # 유효한 데이터일 경우, 데이터 추출
            token = serializer.validated_data['token']
            device_os = serializer.validated_data['device_os']

            # 중복 토큰 검사
            token_exists = DeviceToken.objects.filter(token=token, device_os=device_os)

            if not token_exists: # 토큰이 중복되지 않는 경우, 토큰 저장
                serializer.save()
                return Response({'message': '토큰이 저장되었습니다.'}, status=status.HTTP_201_CREATED)
            else: # 토큰이 중복되는 경우, update_time 갱신
                token_exists.update_time = timezone.now()
                token_exists.save()
                return Response({'message': '토큰이 갱신되었습니다.'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)