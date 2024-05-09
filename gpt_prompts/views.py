from datetime import datetime, timedelta
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from drf_spectacular.utils import extend_schema
from .serializers import *
from .models import GptPrompt
from openai import OpenAI
from kluck_env import env_settings as env
import json

# Create your views here.

# 오늘의 한마디 프롬프트
# api/v1/prompt/today
class PromptToday(APIView):
    '''
    BE-GPT101(GET): 오늘의 한마디에 사용되는 최신(마지막 gpt_id) 프롬프트 메세지 로드\n
    BE-GPT102(POST): 오늘의 한마디에 사용되는 최신(마지막 gpt_id) 프롬프트 메세지 저장
    '''
    serializer_class = PromptTodaySerializer

    @extend_schema(tags=['PromptMsg'])
    def get(self, request):
        # 업데이트하는 방식 X, 프롬프트 메세지 이름 사용 X
        try:
            category = "today"
            latest_today = GptPrompt.objects.filter(category=category).order_by('-gpt_id').first()
            serializer = PromptTodaySerializer(latest_today)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except GptPrompt.DoesNotExist:
            return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

    # 프롬프트 메세지 수정 - 추가하는 방식
    @extend_schema(tags=['PromptMsg'])
    def post(self, request):
        now = datetime.now()
        today = now.strftime('%Y%m%d')
        admins_id = 1
        serializer = PromptTodaySerializer(data=request.data, context={'admins_id': admins_id})

        if serializer.is_valid():
            category = 'today'
            prompt_msg_name = today
            create_date = today
            last = now + timedelta(days=7)
            last_date = last.strftime('%Y%m%d')

            serializer.save(category=category, prompt_msg_name=prompt_msg_name,
                            create_date=create_date, last_date=last_date, admins_id=admins_id)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

# 띠별 운세 프롬프트
# api/v1/prompt/zodiac
class PromptZodiac(APIView):
    '''
    BE-GPT201(GET): 띠별 운세에 사용되는 최신(마지막 gpt_id) 프롬프트 메세지 로드\n
    BE-GPT202(POST): 띠별 운세에 사용되는 최신(마지막 gpt_id) 프롬프트 메세지 저장
    '''
    serializer_class = PromptZodiacSerializer

    @extend_schema(tags=['PromptMsg'])
    def get(self, request):
    # 업데이트하는 방식 X, 프롬프트 메세지 이름 사용 X
        try:
            category = "zodiac"
            latest_zodiac = GptPrompt.objects.filter(category=category).order_by('-gpt_id').first()
            serializer = PromptZodiacSerializer(latest_zodiac)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except GptPrompt.DoesNotExist:
            return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

    # 프롬프트 메세지 수정 - 추가하는 방식
    @extend_schema(tags=['PromptMsg'])
    def post(self, request):
        now = datetime.now()
        today = now.strftime('%Y%m%d')
        admins_id = 1
        serializer = PromptZodiacSerializer(data=request.data, context={'admins_id': admins_id})

        if serializer.is_valid():
            category = 'zodiac'
            prompt_msg_name = today
            create_date = today
            last = now + timedelta(days=7)
            last_date = last.strftime('%Y%m%d')

            serializer.save(category=category, prompt_msg_name=prompt_msg_name,
                            create_date=create_date, last_date=last_date, admins_id=admins_id)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)


# 별자리별 운세 프롬프트
# api/v1/prompt/star
class PromptStar(APIView):
    '''
    BE-GPT301(GET): 별자리별 운세에 사용되는 최신(마지막 gpt_id) 프롬프트 메세지 로드\n
    BE-GPT302(POST): 별자리별 운세에 사용되는 최신(마지막 gpt_id) 프롬프트 메세지 저장
    '''
    serializer_class = PromptStarSerializer

    @extend_schema(tags=['PromptMsg'])
    def get(self, request):
        # 업데이트하는 방식 X, 프롬프트 메세지 이름 사용 X
        # api/v1/prompt/star
        try:
            category = "star"
            latest_star = GptPrompt.objects.filter(category=category).order_by('-gpt_id').first()
            serializer = PromptStarSerializer(latest_star)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except GptPrompt.DoesNotExist:
            return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

    # 프롬프트 메세지 수정 - 추가하는 방식
    @extend_schema(tags=['PromptMsg'])
    def post(self, request):
        now = datetime.now()
        today = now.strftime('%Y%m%d')
        admins_id = 1
        serializer = PromptStarSerializer(data=request.data, context={'admins_id': admins_id})

        if serializer.is_valid():
            category ='star'
            prompt_msg_name = today
            create_date = today
            last = now + timedelta(days=7)
            last_date = last.strftime('%Y%m%d')

            serializer.save(category=category, prompt_msg_name=prompt_msg_name,
                            create_date=create_date, last_date=last_date, admins_id=admins_id)
            return Response(serializer.data, status=status.HTTP_200_OK)


# MBTI별 운세 프롬프트
# api/v1/prompt/mbti
class PromptMbti(APIView):
    '''
    BE-GPT401(GET): MBTI별 운세에 사용되는 최신(마지막 gpt_id) 프롬프트 메세지 로드\n
    BE-GPT402(POST): MBTI별 운세에 사용되는 최신(마지막 gpt_id) 프롬프트 메세지 저장
    '''
    serializer_class = PromptMbtiSerializer

    @extend_schema(tags=['PromptMsg'])
    def get(self, request):
        # 업데이트하는 방식 X, 프롬프트 메세지 이름 사용 X
        try:
            category = "mbti"
            latest_mbti = GptPrompt.objects.filter(category=category).order_by('-gpt_id').first()
            serializer = PromptMbtiSerializer(latest_mbti)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except GptPrompt.DoesNotExist:
            return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

    # 프롬프트 메세지 수정 - 추가하는 방식
    @extend_schema(tags=['PromptMsg'])
    def post(self, request):
        now = datetime.now()
        today = now.strftime('%Y%m%d')
        admins_id = 1
        serializer = PromptMbtiSerializer(data=request.data, context={'admins_id': admins_id})

        if serializer.is_valid():
            category ='MBTI'
            prompt_msg_name = today
            create_date = today
            last = now + timedelta(days=7)
            last_date = last.strftime('%Y%m%d')

            serializer.save(category=category, prompt_msg_name=prompt_msg_name,
                            create_date=create_date, last_date=last_date, admins_id=admins_id)
            return Response(serializer.data, status=status.HTTP_200_OK)


# api/v1/prompt/<str:category>/history
class PromptHistory(APIView):
    '''
    BE-GPT103(203, 303, 403): 입력받는 카테고리에 해당하는 프롬프트 메세지 전체 로드
    '''
    serializer_class = PromptHistorySerializer

    @extend_schema(tags=['PromptMsg'])
    def get(self, request, category):
        try:
            prompt_msgs = GptPrompt.objects.filter(category=category)
            serializer = self.get_serializer(prompt_msgs, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except GptPrompt.DoesNotExist:
            return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)



# api/v1/prompt/test
class GptApiTest(APIView):


    @extend_schema(tags=['PromptMsg'])
    def post(self, request):
        api_key = env.API_KEY
        gpt_client = OpenAI(api_key=api_key)
        category = request.data.get('category')
        prompt_msg = GptPrompt.objects.filter(category=category).order_by('-gpt_id').first()



        if prompt_msg:
            gpt_id = PromptGptApiSerializer(prompt_msg).data['gpt_id']
            prompt = PromptGptApiSerializer(prompt_msg).data['prompt_msg']
            # prompt = prompt
            prompt = prompt + f"출력 양식을 다음과 같이 해 {{\n'luck_date': '20240508',\n 'category': '{category}',\n'attribute2': '각각의 답변 문장에 대한 번호',\n'luck_msg': '질문에 대한 답변',\n'gpt_id': '{gpt_id}'\n}}\n"
            # prompt = prompt + "각각 2문장으로 작성하고 한 문장이 끝나면 문장 마지막에 ###를 표시해"
        else:
            prompt = {}

        # LuckMessage_data_schema = {
        #     "type": "object",
        #     "properties": {
        #         "luck_date": {
        #             "type": "string",
        #             "description": "날짜를 20240428과 같은 양식으로 보여줘",
        #         },
        #         "category": {
        #             "type": "string",
        #             "description": category
        #         },
        #         "attribute2": {
        #             "type": "string",
        #             "description": "각각의 답변 문장에 대한 번호"
        #         },
        #         "luck_msg": {
        #             "type": "string",
        #             "description": "질문에 대한 답변"
        #         },
        #         "gpt_id": {
        #             "type": "string",
        #             "description": gpt_id
        #         }
        #     },
        #     "required": ["luck_date", "category", "attribute2", "luck_msg", "gpt_id"]
        # }

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
                # model="gpt-3.5-turbo-0125",
                model="gpt-4-1106-preview",
                messages=messages,
                temperature=0.5,

                # # response_format 지정하기
                response_format={"type": "json_object"},
            )

            print("response:", response)
            print("message:", response.choices[0].message.content)
            luckmessage = response.choices[0].message.content
            # luckmessages = luckmessage.split('###')
            print(luckmessage)

        luckmessage_data = {'luck_date': '20240508', 'category': category, 'luck_msg': luckmessage, 'gpt_id': gpt_id}
        # luckMsg = {'luck_date': '20240508', 'category': category, 'attribute2':'', 'luck_msg':'', 'gpt_id':''}
        serializer = PromptLuckSerializer(data=luckmessage_data)

        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            raise ParseError(serializer.errors)



# class Test(APIView):
#     api_key = env.API_KEY
#     gpt_client = OpenAI(api_key=api_key)
#     def get_current_weather(location, unit="fahrenheit"):
#         weather_info = {
#             "location": location,
#             "temperature": "",
#             "unit": unit,
#             "forecast": ["sunny", "windy"],
#         }
#         return json.dumps(weather_info)
#
#     messages = [{"role": "user", "content": "지금 서울날씨를 섭씨로 알려줘."}]
#     functions = [
#         {
#             "name": "get_current_weather",
#             "description": "특정 지역의 날씨를 알려줍니다.",
#             "parameters": {
#                 "type": "object",
#                 "properties": {
#                     "location": {
#                         "type": "string",
#                         "description": "지역이름 eg. 서울, 부산, 제주도",
#                     },
#                     "unit": {"type": "string", "enum": ["섭씨", "화씨"]},
#                 },
#                 "required": ["location"],
#             },
#         }
#     ]
#     response = gpt_client.chat.completions.create(
#         model="gpt-3.5-turbo-0613",
#         messages=messages,
#         functions=functions,
#         function_call="auto",
#     )
#     response_message = response.choices[0].message
#     # response.choices[0].message.content
#
#     print('response_message:', response_message)
#
#     if response_message.function_call:
#         # Note: the JSON response may not always be valid; be sure to handle errors
#         available_functions = {
#             "get_current_weather": get_current_weather,
#         }
#         function_name = response_message.function_call.name
#         fuction_to_call = available_functions[function_name]
#         function_args = json.loads(response_message.function_call.arguments)
#         function_response = fuction_to_call(
#             location=function_args.get("location"),
#             unit=function_args.get("unit"),
#         )
#
#         messages.append(response_message)
#         messages.append(
#             {
#                 "role": "function",
#                 "name": function_name,
#                 "content": function_response,
#             }
#         )
#         second_response = gpt_client.chat.completions.create(
#             model="gpt-3.5-turbo-0613",
#             messages=messages,
#         )  # get a new response from GPT where it can see the function response
#
#         json_data = json.dumps(second_response.choices[0].message.content, ensure_ascii=False)
#
#         print('second_response:', second_response)

