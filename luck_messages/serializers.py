from rest_framework.serializers import ModelSerializer
from .models import LuckMessage


class mbtiSerializer(ModelSerializer):
    class Meta:
        model = LuckMessage
        # fields = '__all__'  # 모든 필드 포함
        fields = ('luck_date', 'category', 'attribute1', 'luck_msg')