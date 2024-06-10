from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
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
            # first()로 row의 존재여부 확인 row가 없으면 예외발생하지 않고 None반환!
            pushtime = AdminSetting.objects.first()
            if pushtime:
                serializer = Admin_settingsSerializer(pushtime)
                response_serializer = Admin_settingsSerializer(serializer.instance, fields=('push_time',))
                return Response(response_serializer.data, status=status.HTTP_200_OK)
                # return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response('push_time이 없습니다.', status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'Error':'오류가 있습니다.'}, status=status.HTTP_404_NOT_FOUND)

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
        try:
            # insert or update
            # targetrow의 값을 통해 새로운 row를 생성하는 것이 아닌 기존의 row를 선택
            targetrow = AdminSetting.objects.first()

            if targetrow:
                # update
                # 관리자 세팅과 관련 값은 하나만 유지하기로 했기에 1번 row로 설정
                # partial=True 옵션으로 row전체 update가 아닌 일부만 update
                serializer = Admin_settingsSerializer(targetrow, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    response_serializer = Admin_settingsSerializer(serializer.instance, fields=('push_time',))
                    return Response(response_serializer.data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
            else:
                # 객체가 존재하지 않을 경우
                # insert
                serializer = Admin_settingsSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    response_serializer = Admin_settingsSerializer(serializer.instance, fields=('push_time',))
                    return Response(response_serializer.data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'Error':'오류가 있습니다.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
