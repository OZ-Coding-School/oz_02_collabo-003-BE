from rest_framework.serializers import ModelSerializer
from luck_messages.models import LuckMessage
from .models import Admin

#/api/v1/admin/login
class AdminLoginSerializer(ModelSerializer):
    '''
    프론트에서 admin_id(ID), user_pw(패스워드)를 받아 로그인,
    관리자 로그인 후 최종 접속 날짜(last_date)를 오늘 날짜로 업데이트
    '''
    class Meta:
        model = Admin
        fields = ('admin_id', 'admin_pw')

#/api/v1/admin/
class AdminSerializer(ModelSerializer):
    class Meta:
        model = Admin
        fields = ('admins_id', 'admin_user', 'cell_num', 'email', 'create_date', 'last_date')

#/api/v1/admin/signup/
class AdminSignupSerializer(ModelSerializer):
    '''
    피그마 화면에서 수정이 가능한 항목만 수정
    '''
    class Meta:
        model = Admin
        # fields = '__all__'  # 모든 필드 포함
        # fields = ('msg_id', 'luck_date', 'category', 'attribute2', 'luck_msg')
        fields = ('admin_id', 'admin_user', 'cell_num', 'email', 'admin_pw')


#/api/v1/admin/msg/
class LuckMessageSerializer(ModelSerializer):
    #메세지 수정
    class Meta:
        model = LuckMessage
        # fields = '__all__'  # 모든 필드 포함
        fields = ('msg_id', 'luck_msg')
