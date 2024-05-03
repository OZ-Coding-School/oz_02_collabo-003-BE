from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import authenticate, login
from django.utils import timezone
from luck_messages.models import LuckMessage
from admins.models import Admin
from .serializers import *


# api/v1/admin/login/
class AdminLogin(APIView):
    '''
    프론트에서 admin_id(ID), admin_pw(패스워드)를 받아 로그인,
    관리자 로그인 후 최종 접속 날짜(last_date)를 오늘 날짜로 업데이트
    '''
    serializer_class = AdminLoginSerializer
    def post(self, request):
        admin_id = request.data.get('admin_id')
        admin_pw = request.data.get('admin_pw')

        try:
            admin = Admin.objects.get(admin_id=admin_id)
            if check_password(admin_pw, admin.admin_pw):
                # 비밀번호 확인 후 로그인 처리
                admin.last_date = timezone.now()
                admin.save()
                return Response({'message': '로그인 성공'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': '비밀번호가 일치하지 않습니다.'}, status=status.HTTP_401_UNAUTHORIZED)
        except Admin.DoesNotExist:
            return Response({'message': '존재하지 않는 관리자 ID입니다.'}, status=status.HTTP_404_NOT_FOUND)

          
# api/vi/admin/
class AdminUsers(APIView):
    '''
    프론트에서 admins_id(PK), email, admin_user(사용자명), cell_num(폰 번호), create_date(등록일)를 로드
    '''
    serializer_class = AdminSerializer
    def get(self, request):
        admins = Admin.objects.all()
        serializer = AdminSerializer(admins, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# api/v1/admin/signup/
class AdminUsersSignup(APIView):
    '''
    프론트에서 admin_id(ID), admin_user(사용자명), cell_num(폰 번호), email, user_pw(패스워드)를 받아
    관리자 등록 수정 내용을 따로 다시 반환하지는 않는다.
    '''
    serializer_class = AdminSignupSerializer
    def post(self, request):

        password = request.data.get('admin_pw')
        serializer = AdminSignupSerializer(data=request.data)

        try:
            validate_password(password)
        except:
            raise ParseError('Password is invalid.')

        if serializer.is_valid():
            user = serializer.save()
            user.admin_pw = make_password(password)
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

