from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from luck_messages.models import LuckMessage
from .models import kluck_Admin

#/api/v1/admin/login
class AdminLoginSerializer(ModelSerializer):
    '''
    프론트에서 admin_id(ID), user_pw(패스워드)를 받아 로그인,
    관리자 로그인 후 최종 접속 날짜(last_date)를 오늘 날짜로 업데이트
    '''
    username = serializers.CharField(source='user.username')
    password = serializers.CharField(source='user.password')
    class Meta:
        model = kluck_Admin
        fields = ('username', 'password')

#/api/v1/admin/
class AdminSerializer(ModelSerializer):

    username = serializers.CharField(source='user.username')
    email = serializers.CharField(source='user.email')
    date_joined = serializers.CharField(source='user.date_joined')
    last_login = serializers.CharField(source='user.last_login')
    class Meta:
        model = kluck_Admin
        fields = ('username', 'cell_num', 'email', 'date_joined', 'last_login')

#/api/v1/admin/signup/
class AdminSignupSerializer(ModelSerializer):
    '''
    피그마 화면에서 수정이 가능한 항목만 수정
    '''
    username = serializers.CharField(source='user.username')
    email = serializers.CharField(source='user.email')
    password = serializers.CharField(source='user.password')
    class Meta:
        model = kluck_Admin
        # fields = '__all__'  # 모든 필드 포함
        # fields = ('msg_id', 'luck_date', 'category', 'attribute2', 'luck_msg')
        fields = ('username', 'cell_num', 'email', 'password')


#/api/v1/admin/msg/
class LuckMessageSerializer(ModelSerializer):
    #메세지 수정
    class Meta:
        model = LuckMessage
        # fields = '__all__'  # 모든 필드 포함
        fields = ('msg_id', 'luck_msg')
