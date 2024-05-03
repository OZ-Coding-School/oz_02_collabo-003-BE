from rest_framework import serializers
from .models import LuckMessage

class TodayLuckSerializer(serializers.ModelSerializer):
    class Meta:
        model = LuckMessage
        fields = ('msg_id', 'luck_date', 'category', 'attribute1', 'attribute2', 'luck_msg')