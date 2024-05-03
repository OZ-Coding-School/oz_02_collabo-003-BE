from rest_framework.serializers import ModelSerializer
from luck_messages.models import LuckMessage

#/api/v1/admin/zodiac/<int:msg_id>/update/
class LuckMessageSerializer(ModelSerializer):
    #메세지 수정
    class Meta:
        model = LuckMessage
        # fields = '__all__'  # 모든 필드 포함
        fields = ('msg_id', 'luck_msg')
