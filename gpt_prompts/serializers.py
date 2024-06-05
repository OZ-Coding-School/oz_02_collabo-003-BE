from rest_framework import serializers
from .models import GptPrompt
from luck_messages.models import LuckMessage

class PromptSerializer(serializers.ModelSerializer):
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


# last_date update를 위한 Serializer
class PromptUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model= GptPrompt
        fields = ('gpt_id', 'category', 'last_date')


# class PromptGptApiSerializer(serializers.ModelSerializer):

#     class Meta:
#         model= GptPrompt
#         fields = ('gpt_id', 'category', 'prompt_msg', 'create_date', 'last_date', 'admins_id')


# class PromptLuckSerializer(serializers.ModelSerializer):

#     class Meta:
#         model= LuckMessage
#         fields = ('luck_date', 'category', 'attribute1', 'attribute2', 'luck_msg', 'gpt_id')
