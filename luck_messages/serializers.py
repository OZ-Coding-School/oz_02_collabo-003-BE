from rest_framework.serializers import ModelSerializer
from .models import LuckMessage

class zodiacSerializer(ModelSerializer):
    class Meta:
        model = LuckMessage
        # fields = '__all__'  # 모든 필드 포함
        fields = ('msg_id', 'luck_date', 'category', 'attribute1', 'attribute2', 'luck_msg')
