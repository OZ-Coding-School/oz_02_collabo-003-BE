from rest_framework import serializers
from .models import GptPrompt

class PromptSerializer(serializers.ModelSerializer):
    # # 임의로 관리자 id가 1인 자료 생성.
    # admins_id = serializers.SerializerMethodField()

    # def get_admins_id(self, obj) -> int:
    #     return 1
    def create(self, validated_data):
        prompt_msg = validated_data.pop('prompt_msg')
        instance = GptPrompt.objects.create(prompt_msg=prompt_msg, **validated_data)
        return instance

    class Meta:
        model = GptPrompt
        fields = '__all__'
# 프롬프트 조회 및 생성 serializer 하나로 합침.

class PromptHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model= GptPrompt
        fields = ('gpt_id', 'category', 'prompt_msg_name', 'prompt_msg', 'create_date', 'last_date')


        
# class PromptGptApiSerializer(serializers.ModelSerializer):

#     class Meta:
#         model= GptPrompt
#         fields = ('gpt_id', 'category', 'prompt_msg', 'create_date', 'last_date', 'admins_id')


# class PromptLuckSerializer(serializers.ModelSerializer):

#     class Meta:
#         model= LuckMessage
#         fields = ('luck_date', 'category', 'attribute1', 'attribute2', 'luck_msg', 'gpt_id')
