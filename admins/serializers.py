from rest_framework.serializers import ModelSerializer
from luck_messages.models import LuckMessage

class StarSerializer(ModelSerializer):
    class Meta:
        model = LuckMessage
        # fields = '__all__'  # 모든 필드 포함
        fields = ('msg_id', 'luck_date', 'category', 'attribute1', 'attribute2', 'luck_msg')