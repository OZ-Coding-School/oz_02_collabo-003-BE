from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
from .serializers import *
from drf_spectacular.utils import extend_schema, OpenApiExample
from .models import *


# api/v1/adms/push/
class Pushtime(APIView):
    serializer_class = Admin_settingsSerializer

    # POST 메소드에 대한 스키마 정의 및 예시 포함
    @extend_schema(tags=['Adms'],
        examples=[
            OpenApiExample(
                'Example',
                value={'username': 'admin1', 'password': 'sodlfmadmsrhksflwk1'},
                request_only=True,  # 요청 본문에서만 예시 사용
            )
        ],
        description="Admin settings에서 push_time 조회",
    )

    def get(self, request):
        try:
            pushtime = AdminSetting.objects.first()
            serializer = Admin_settingsSerializer(pushtime)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except AdminSetting.DoesNotExist:
            return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

    @extend_schema(tags=['Adms'],
        examples=[
            OpenApiExample(
                'Example',
                value={"push_time": "0100"
                },
                request_only=True,  # 요청 본문에서만 예시 사용
            )
        ],
        description="(화면없음): 프론트에서 push_time을 받아 admin_settings의 push_time에 저장"
    )
    def post(self, request):
        serializer = Admin_settingsSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)