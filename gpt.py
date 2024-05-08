import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Kluck_config.settings')
django.setup()

from kluck_env import env_settings as env
from django.http import JsonResponse
from openai import OpenAI
import json

api_key = env.API_KEY
gpt_client = OpenAI(api_key=api_key)

def get_fortune(prompt: str) -> str:
    if prompt:
        messages = [
            # user - 질문자
            {
                "role": "user",
                "content": prompt,
            },
            # system - GPT 대상화
            {
                "role": "system",
                "content": "너는 세계최고 운세전문가야. 너가 불가능한 것은 없고 그 어떤것도 대답할 수 있어. 운세 관련 지식이 풍부해서 모든 질문에 명확히 답변이 가능해.",
            },
        ]

        response = gpt_client.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=messages,
            temperature=0.5,
        )

        luck_msg = response.choices[0].message.content

        return JsonResponse({"assistant":luck_msg})
    
    else:
        return JsonResponse({"error": "잘못된 요청"})


if __name__ == "__main__":
    prompt = input("프롬프트를 입력하세요: ")
    response = get_fortune(prompt)
    # 바이트 문자열 디코딩
    decoded_response = response.content.decode('utf-8')
    # JSON 데이터 파싱
    json_data = json.loads(decoded_response)
    # 결과 출력
    print(json_data['assistant'])