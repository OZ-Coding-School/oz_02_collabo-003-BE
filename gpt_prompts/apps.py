from django.apps import AppConfig


class GptPromptConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "gpt_prompts"
    verbose_name = "GPT API를 이용한 오늘의 한마디 데이터 자동 저장"
