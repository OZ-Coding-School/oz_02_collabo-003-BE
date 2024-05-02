from rest_framework.serializers import ModelSerializer
from luck_messages.models import LuckMessage


#/api/v1/admin/today/<int:msg_id>/
class TodaySerializer(ModelSerializer):
    '''
    피그마 화면에서 수정이 가능한 항목만 수정
    '''
    class Meta:
        model = LuckMessage
        # fields = '__all__'  # 모든 필드 포함
        # fields = ('msg_id', 'luck_date', 'category', 'attribute2', 'luck_msg')
        fields = ('msg_id', 'luck_msg')