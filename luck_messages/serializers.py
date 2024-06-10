from rest_framework import serializers
from .models import LuckMessage

class TodayLuckSerializer(serializers.ModelSerializer):
    #오늘 날짜의 Today, 띠, 별, MBTI 메세지 조회
    class Meta:
        model = LuckMessage
        fields = ('luck_date', 'category', 'attribute1', 'attribute2', 'luck_msg')


class TodaySerializer(serializers.ModelSerializer):
    #특정 일자의 Today 메세지 조회
    class Meta:
        model = LuckMessage
        # fields = '__all__'  # 모든 필드 포함
        fields = ('msg_id', 'luck_date', 'category', 'attribute2', 'luck_msg', 'gpt_id')


class ZodiacSerializer(serializers.ModelSerializer):
    #특정 일자의 띠 메세지 조회
    class Meta:
        model = LuckMessage
        # fields = '__all__'  # 모든 필드 포함
        fields = ('msg_id', 'luck_date', 'category', 'attribute1', 'attribute2', 'luck_msg', 'gpt_id')


class StarSerializer(serializers.ModelSerializer):
    #특정 일자의 별자리 메세지 조회
    class Meta:
        model = LuckMessage
        # fields = '__all__'  # 모든 필드 포함
        fields = ('msg_id', 'luck_date', 'category', 'attribute1', 'attribute2', 'luck_msg', 'gpt_id')


class MbtiSerializer(serializers.ModelSerializer):
    #특정 일자의 MBTI 메세지 조회
    class Meta:
        model = LuckMessage
        # fields = '__all__'  # 모든 필드 포함
        fields = ('msg_id', 'luck_date', 'category', 'attribute1', 'luck_msg', 'gpt_id')

class GptLuckSerializer(serializers.ModelSerializer):
    # GPT에게 질문하고 받는 운세 데이터 저장용.
    class Meta:
        model = LuckMessage
        fields = ('msg_id', 'luck_date', 'category', 'attribute1', 'attribute2', 'luck_msg', 'gpt_id')