from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiResponse
from .serializers import *

# api/v1/admin/login/
# JWT로그인 클래스
class JWTLogin(APIView):
    serializer_class = LoginSerializer
    permission_classes = (AllowAny,)
    @extend_schema(tags=['Admin'],
        examples=[
            OpenApiExample(
                'Example',
                value={'username': 'admin', 'password': 'sksmsrhksflwk1'},
                request_only=True,  # 요청 본문에서만 예시 사용
            )
        ],
        description="JWT Login"
    )
    # post로 로그인
    def post(self, request, *args, **kwargs):
        # 시리얼라이져로 로그인 정보 받기
        serializer = LoginSerializer(data=request.data)
        # 시리얼러이져로 로그인 데이터 검증
        if serializer.is_valid():
            # 로그인 유저가 있는지 확인하고 user에 대입
            user = serializer.validated_data['user']
            # user로 리플래시토큰을 생성하고 refresh에 대입
            refresh = RefreshToken.for_user(user)
            # response를 딕셔너리 형식으로 'refresh': refreshtoken, 'access': accesstoken 정보를 반환
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        # 데이터 검증 실패하면 오류 코드 반환
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# api/v1/admin/refresh/
class JWTRefresh(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = ()

    @extend_schema(
        tags=['Admin'],
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'refresh': {'type': 'string'},
                },
                'required': ['refresh'],
            }
        },
        responses={
            200: OpenApiResponse(
                response={
                    'type': 'object',
                    'properties': {
                        'access': {'type': 'string'},
                    },
                    'example': {
                        'access': 'new access token'
                    }
                }
            ),
            401: OpenApiResponse(
                response={
                    'type': 'object',
                    'properties': {
                        'detail': {'type': 'string'},
                    },
                    'example': {
                        'detail': 'Invalid token'
                    }
                }
            )
        },
        description="Check and refresh tokens"
    )
    def post(self, request, *args, **kwargs):
        refresh_token = request.data.get('refresh')

        # refresh_token이 없으면 refresh_token이 필요하다고 오류 반환
        if not refresh_token:
            return Response({'detail': 'Refresh token이 없습니다.'},status=status.HTTP_400_BAD_REQUEST)

        try:
            # request로 받은 refresh_token으로 RefreshToken 객체 생성
            refresh = RefreshToken(refresh_token)
            # RefreshToken 객체에서 새로운 access_token 생성
            new_access_token = str(refresh.access_token)
            # response로 access_token 반환
            return Response({'access': new_access_token})
        except TokenError:
            return Response({'detail': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)

# api/vi/admin/
class AdminUsers(APIView):
    '''
    BE-ADM003: 프론트에서 admins_id(PK), email, admin_user(사용자명), cell_num(폰 번호), create_date(등록일)를 로드
    '''
    serializer_class = AdminSerializer
    @extend_schema(tags=['Admin'],)

    def get(self, request):
        admins = kluck_Admin.objects.all()
        serializer = AdminSerializer(admins, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# api/v1/admin/msg/
class EditLuckMessage(APIView):
    serializer_class = LuckMessageSerializer
    @extend_schema(tags=['AdminMsg'],
        examples=[
            OpenApiExample(
                'Example',
                value={"msg_id": "2694",
                        "luck_msg": "오늘은 아이유 좋은날 들어요. 오늘은 좋은날이니까"
                },
                request_only=True,  # 요청 본문에서만 예시 사용
            )
        ],
        description="BE-GPT105(205, 305, 405): 프론트에서 msg_id를 받아 luck_messages의 모델에서 해당 id를 찾아 내용 수정\n수정 내용을 따로 다시 반환하지는 않는다."
    )
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