from rest_framework.serializers import ModelSerializer
from .models import LuckMessage

class todaySerializer(ModelSerializer):
  #특정 일자의 Today메세지 조회
    class Meta:
        model = LuckMessage
        # fields = '__all__'  # 모든 필드 포함
        fields = ('msg_id', 'luck_date', 'category', 'attribute2', 'luck_msg')

        
class mbtiSerializer(ModelSerializer):
  #특정 일자의 MBTI메세지 조회
    class Meta:
        model = LuckMessage
        # fields = '__all__'  # 모든 필드 포함
        fields = ('msg_id', 'luck_date', 'category', 'attribute1', 'luck_msg')

        
class zodiacSerializer(ModelSerializer):
    class Meta:
        model = LuckMessage
        # fields = '__all__'  # 모든 필드 포함
        fields = ('luck_date', 'category', 'attribute1', 'attribute2', 'luck_msg')

        
class starSerializer(ModelSerializer):
  #특정 일자의 별자리 메세지 조회
    class Meta:
        model = LuckMessage
        # fields = '__all__'  # 모든 필드 포함
        fields = ('msg_id', 'luck_date', 'category', 'attribute1', 'luck_msg')


class TodayLuckSerializer(ModelSerializer):
  #오늘 날짜의 Today, 띠, 별, MBTI 메세지 조회
    class Meta:
        model = LuckMessage
        fields = ('msg_id', 'luck_date', 'category', 'attribute1', 'attribute2', 'luck_msg')