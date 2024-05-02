from rest_framework import serializers
from .models import GptPrompt

class PromptTodaySerializer(serializers.ModelSerializer):
    # 임의로 관리자 id가 1인 자료 생성.
    admins_id = serializers.SerializerMethodField()

    def get_admins_id(self, obj):
        return 1
    
    def create(self, validated_data):
        prompt_msg = validated_data.pop('prompt_msg')
        instance = GptPrompt.objects.create(prompt_msg=prompt_msg, **validated_data)
        return instance

    class Meta:
        model = GptPrompt
        fields = '__all__'