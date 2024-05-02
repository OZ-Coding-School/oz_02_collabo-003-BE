from rest_framework.serializers import ModelSerializer
from .models import LuckMessage
from rest_framework import serializers


class zodiacSerializer(ModelSerializer):
    class Meta:
        model = LuckMessage
        # fields = '__all__'  # 모든 필드 포함
        fields = ('luck_date', 'category', 'attribute1', 'attribute2', 'luck_msg')

        
class starSerializer(ModelSerializer):
    class Meta:
        model = LuckMessage
        # fields = '__all__'  # 모든 필드 포함
        fields = ('luck_date', 'category', 'attribute1', 'luck_msg')


class TodayLuckSerializer(serializers.ModelSerializer):

    class Meta:
        model = LuckMessage
        fields = ('luck_date', 'category', 'attribute1', 'attribute2', 'luck_msg')

