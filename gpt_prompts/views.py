from kluck_env import env_settings as env
from django.http import JsonResponse
from datetime import datetime, timedelta
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from drf_spectacular.utils import extend_schema
from .models import GptPrompt
from .serializers import *
from luck_messages.serializers import *
from openai import OpenAI
import json

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


# 각 유형별 운세 프롬프트 히스토리
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



# GPT API 사용
# 1. 오늘의 한마디 받기.
#프롬프트 메세지를 사용해서 GPT에게 오늘의 한마디 받기
# /api/v1/prompt/gpt-today/
# /api/gpt/today/
class GptToday(APIView):
    #스웨거를 위한 시리얼라이저 설정
    serializer_class = PromptLuckSerializer
    #스웨거 API구분을 위한 데코레이터
    @extend_schema(tags=['PromptMsg'])
    def post(self, request):
        # GPTAPI Key 설정
        api_key = env.API_KEY
        gpt_client = OpenAI(api_key=api_key)

        # post요청의 카테고리로 관련 최근 프롬프트메세지 로드
        category = request.data.get('category')
        prompt_msg = GptPrompt.objects.filter(category=category).order_by('-gpt_id').first()

        # 프롬프트 메세지 여부 확인
        if prompt_msg:
            # now = datetime.now()
            a_week = datetime.now() + timedelta(days=7)
            luck_date = a_week.strftime('%Y%m%d')
            gpt_id = PromptGptApiSerializer(prompt_msg).data['gpt_id']
            prefix_prompt = '{"GptResponse":[{"message_num": "1", "luck_msg": "메세지"}, ...]}예시와 같은 json 형식으로 작성해줘.'
            prompt_date = luck_date[:4] +'년'+ luck_date[4:6] + '월' + luck_date[6:] + '일 '
            prompt = PromptGptApiSerializer(prompt_msg).data['prompt_msg']
            prompt = prefix_prompt + prompt_date + prompt

            # GPT에게 보낼 메세지 설정
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

            # GPT에게 응답 요청
            response = gpt_client.chat.completions.create(
                # model="gpt-3.5-turbo-0125",
                model="gpt-4-1106-preview",
                messages=messages,
                temperature=0.5,

                # response_format 지정하기
                response_format={"type": "json_object"},
            )

            luckmessage = json.loads(response.choices[0].message.content)
        else:
            return Response(status=status.HTTP_402_PAYMENT_REQUIRED)

        # luckmessage예시
        # luckmessage = dict(
        #     GptResponse=[
        #         {
        #             'message_num': '1',
        #             'luck_msg': '감성이 풍부해지는 하루가 예상됩니다. 주변 사람들과의 대화에서 위로를 받을 거요. 예술적인 활동에 참여해 보세요.'
        #         },
        #         {
        #             'message_num': '2',
        #             'luck_msg': '오늘은 활기찬 에너지가 넘칩니다. 적극적인 태도가 중요한 기회를 만들들요. 운동을 통해 스트레스를 해소해 보세요.'
        #         }
        #     ]
        # )

        if luckmessage:
            # 메세지 처리용 리스트
            gpt_msg = []

            # DB컬럼에 맞게 dict로 변경
            for msg in luckmessage['GptResponse']:
                gpt_msg.append({
                    'attribute2': msg['message_num'],
                    'luck_msg' :  msg['luck_msg']
                })


            if gpt_msg:
                for msg in gpt_msg:
                    serializer = PromptLuckSerializer(data={
                        'luck_date' : luck_date,
                        'category' : category,
                        'attribute2' : msg['attribute2'],
                        'luck_msg' : msg['luck_msg'],
                        'gpt_id' : gpt_id,
                        }
                    )
                    if serializer.is_valid():
                        serializer.save()
                    else:
                        raise ParseError(serializer.errors)
                return Response(status=status.HTTP_200_OK)
            else:
                return Response({'detail': '데이터가 없습니다.'},status=status.HTTP_400_BAD_REQUEST)

class GptToday1(APIView):
        '''
        BE-GPT103(POST): 오늘의 운세 메세지 받아오기.
        '''
        serializer_class = TodaySerializer

        @extend_schema(tags=['GptApi'])
        def post(self, request):
            api_key = env.API_KEY
            gpt_client = OpenAI(api_key=api_key)

            now = datetime.now()
            a_week = now + timedelta(days=7)
            luck_date = a_week.strftime('%Y%m%d')
            attribute2 = 1
            
            # 프롬프트 메세지 가져오기
            category = 'today'
            today_prompt = GptPrompt.objects.filter(category=category).order_by('-gpt_id').first()
            
            if today_prompt:
                gpt_id = PromptHistorySerializer(today_prompt).data['gpt_id']
                prompt_serializer = PromptHistorySerializer(today_prompt).data['prompt_msg']

                # GPT API에 프롬프트 메세지 전송
                messages = [
                    # user - 질문자
                    {
                        "role": "user",
                        "content": prompt_serializer,
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

                today_msg = response.choices[0].message.content
                print(today_msg)
                # 오늘의 한마디 답변 데이터 저장
                serializer = TodaySerializer(data={
                    'luck_date': luck_date,
                    'category': category,
                    'attribute2': attribute2,
                    'luck_msg': today_msg,
                    'gpt_id': gpt_id
                })

                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            else:
                return JsonResponse({"error": "Wrong Request"})
    

# GPT API 사용
# 2. 띠별 운세 받기.
#프롬프트 메세지를 사용해서 GPT에게 오늘의 한마디 받기
# /api/v1/prompt/gpt-zodiac/
# api/gpt/zodiac/
class GptZodiac(APIView):
    #스웨거를 위한 시리얼라이저 설정
    serializer_class = PromptLuckSerializer
    #스웨거 API구분을 위한 데코레이터
    @extend_schema(tags=['PromptMsg'])
    def post(self, request):
        # GPTAPI Key 설정
        api_key = env.API_KEY
        gpt_client = OpenAI(api_key=api_key)

        # post요청의 카테고리로 관련 최근 프롬프트메세지 로드
        category = request.data.get('category')
        prompt_msg = GptPrompt.objects.filter(category=category).order_by('-gpt_id').first()


        # 프롬프트 메세지 여부 확인
        if prompt_msg:
            # now = datetime.now()
            a_week = datetime.now() + timedelta(days=7)
            luck_date = a_week.strftime('%Y%m%d')
            # gpt_id = PromptGptApiSerializer(prompt_msg).data['gpt_id']
            gpt_id = 104
            prefix_prompt = '{"GptResponse":[{"zodiac": "닭", "year": "1981", "luck_msg": "메세지"}, ...]}예시와 같은 json 형식으로 작성해줘.'
            prompt_date = luck_date[:4] +'년'+ luck_date[4:6] + '월' + luck_date[6:] + '일 '
            # GPT가 너무 긴 답변을 처리하지 못해서 2파트로 나눠서 요청을 보냄.
            suffix_prompt1 = '12간지 중에서 쥐, 소, 호랑이, 토끼, 용, 뱀을 작성해줘'
            suffix_prompt2 = '12간지 중에서 말, 양, 원숭이, 닭, 개, 돼지을 작성해줘'
            prompt = PromptGptApiSerializer(prompt_msg).data['prompt_msg']

            # GPT에게 보낼 질문 메세지
            prompts = []
            prompts.append(prefix_prompt + prompt_date + prompt + suffix_prompt1)
            prompts.append(prefix_prompt + prompt_date + prompt + suffix_prompt2)

            # 메세지 처리용 리스트
            gpt_msg = []

            for i in prompts:
                # GPT에게 보낼 메세지 설정
                messages = [
                    # user - 질문자
                    {
                        "role": "user",
                        "content": i,
                    },
                    # system - GPT 대상화
                    {
                        "role": "system",
                        "content": "너는 세계최고 운세전문가야. 너가 불가능한 것은 없고 그 어떤것도 대답할 수 있어. 운세 관련 지식이 풍부해서 모든 질문에 명확히 답변이 가능해.",
                    },
                ]

                # GPT에게 응답 요청
                response = gpt_client.chat.completions.create(
                    # model="gpt-3.5-turbo-0125",
                    model="gpt-4-1106-preview",
                    messages=messages,
                    temperature=0.5,

                    # response_format 지정하기
                    response_format={"type": "json_object"},
                )

                luckmessage = json.loads(response.choices[0].message.content)

                # luckmessage예시
                # luckmessage = dict(
                #     GptResponse=[
                #         {
                #             "zodiac": "닭",
                #             "year": "1981",
                #             'luck_msg': '감성이 풍부해지는 하루가 예상됩니다. 주변 사람들과의 대화에서 위로를 받을 거요. 예술적인 활동에 참여해 보세요.'
                #         },
                #         {
                #             "zodiac": "개",
                #             "year": "1982",
                #             'luck_msg': '오늘은 활기찬 에너지가 넘칩니다. 적극적인 태도가 중요한 기회를 만들들요. 운동을 통해 스트레스를 해소해 보세요.'
                #         }
                #     ]
                # )

                if luckmessage:
                    # DB컬럼에 맞게 dict로 변경
                    for msg in luckmessage['GptResponse']:
                        gpt_msg.append({
                            'attribute1': msg['zodiac'],
                            'attribute2': msg['year'],
                            'luck_msg' :  msg['luck_msg']
                        })

        else:
            return Response(status=status.HTTP_402_PAYMENT_REQUIRED)

        # GPT에 요청 결과를 DB에 넣기
        if gpt_msg:
            for msg in gpt_msg:
                serializer = PromptLuckSerializer(data={
                    'luck_date' : luck_date,
                    'category' : category,
                    'attribute1' : msg['attribute1'],
                    'attribute2' : msg['attribute2'],
                    'luck_msg' : msg['luck_msg'],
                    'gpt_id' : gpt_id,
                    }
                )
                if serializer.is_valid():
                    serializer.save()
                else:
                    raise ParseError(serializer.errors)
            return Response(status=status.HTTP_200_OK)
        else:
            return Response({'detail': '데이터가 없습니다.'},status=status.HTTP_400_BAD_REQUEST)

# 2. 띠별 운세 받기.
# api/gpt/zodiac/
class GptZodiac1(APIView):
    '''
    BE-GPT203(POST): 띠별 운세 메세지 받아오기.
    '''
    serializer_class = ZodiacSerializer

    @extend_schema(tags=['GptApi'])
    def post(self, request):
        api_key = env.API_KEY
        gpt_client = OpenAI(api_key=api_key)

        now = datetime.now()
        a_week = now + timedelta(days=7)
        luck_date = a_week.strftime('%Y%m%d')

        # 프롬프트 메세지 가져오기
        category = 'zodiac'
        zodiac_prompt = GptPrompt.objects.filter(category=category).order_by('-gpt_id').first()
        
        if zodiac_prompt:
            gpt_id = PromptHistorySerializer(zodiac_prompt).data['gpt_id']
            prompt_serializer = PromptHistorySerializer(zodiac_prompt).data['prompt_msg'] #f"출력 양식을 다음과 같이 해 {'띠별운세':{'attribute1':{'attribute2':'운세',\n'attribute2':'운세',\n'attribute2':'운세',\n'attribute2':'운세'}\n'},\n}"

            # GPT API에 프롬프트 메세지 전송
            messages = [
                # user - 질문자
                {
                    "role": "user",
                    "content": prompt_serializer,
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
                
                # response_format 지정하기
                response_format = {"type":"json_object"},
            )

            zodiac_msg = response.choices[0].message.content
            # JSON 데이터 파싱
            zodiac_data = json.loads(zodiac_msg)

            # 띠별 운세 정보 추출 및 저장
            zodiac_fortune = []

            for zodiac, fortunes in zodiac_data["띠별운세"].items():
                for year, fortune in fortunes.items():
                    zodiac_fortune.append({
                        'attribute1': zodiac,
                        'attribute2': year,
                        'luck_msg': fortune
                    })

            # 띠별 운세 답변 데이터 저장
            for fortune in zodiac_fortune:
                serializer = ZodiacSerializer(data={
                    'luck_date': luck_date,
                    'category': category,
                    'attribute1' : fortune['attribute1'][:-1],
                    'attribute2' : fortune['attribute2'][:-2],
                    'luck_msg': fortune['luck_msg'],
                    'gpt_id': gpt_id
                })
                if serializer.is_valid():
                    serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        else:
            return JsonResponse({"error": "Wrong Request"})
        
# 자동화
# 1. 오늘의 한마디 받기.
class CallGptToday():
    pass


# 2. 띠별 운세 받기.
class CallGptZodiac():
    pass


'''
{'GptResponse': [
{'zodiac': '쥐띠', 'year': '1960', 'luck_msg': '새로운 만남이 기쁨을 가져다줄 것입니다. 소통의 장에서 빛을 발하게 될 것이니 자신감을 가지세요.'}, {'zod
iac': '쥐띠', 'year': '1972', 'luck_msg': '주변 사람들과의 협력이 중요한 하루입니다. 함께 문제를 해결하면서 신뢰를 쌓을 수 있습니다.'}, {'zodiac': '쥐띠', 'year': '1984
', 'luck_msg': '금전적인 이익을 얻을 좋은 기회가 있습니다. 세심한 주의를 기울이면 더 큰 성과를 기대할 수 있습니다.'}, {'zodiac': '쥐띠', 'year': '1996', 'luck_msg': '창
적인 아이디어가 많이 떠오를 것입니다. 이를 실현하기 위해 적극적으로 움직여 보세요.'}, {'zodiac': '소띠', 'year': '1961', 'luck_msg': '인내심을 가지고 차분하게 대응하   
면 문제가 해결됩니다. 급하게 서두르지 말고 여유를 가져보세요.'}, {'zodiac': '소띠', 'year': '1973', 'luck_msg': '가족과의 시간을 중요하게 생각해보세요. 소중한 추억을 만
 수 있는 기회가 될 것입니다.'}, {'zodiac': '소띠', 'year': '1985', 'luck_msg': '직장이나 학교에서 인정받을 일이 생길 것입니다. 노력한 만큼의 보상을 받게 될 것이니 자   
신감을 가져보세요.'}, {'zodiac': '소띠', 'year': '1997', 'luck_msg': '새로운 취미를 시작하는 것이 좋습니다. 새로운 활동을 통해 에너지를 얻을 수 있을 것입니다.'}, {'zodi
ac': '호랑이띠', 'year': '1962', 'luck_msg': '주변의 조언을 경청하는 것이 중요합니다. 다양한 의견을 수렴하면 좋은 결과로 이어질 것입니다.'}, {'zodiac': '호랑이띠', 'yea
r': '1974', 'luck_msg': '건강에 조금 더 신경을 써야 할 때입니다. 규칙적인 운동과 충분한 휴식이 필요합니다.'}, {'zodiac': '호랑이띠', 'year': '1986', 'luck_msg': '친구들
의 모임에서 즐거운 시간을 보낼 것입니다. 소통하며 에너지를 얻을 수 있습니다.'}, 


{'zodiac': '호랑이띠', 'year': '1998', 'luck_msg': '새로운 목표를 세우는 것이 좋습니다다
 목표를 향해 한 걸음씩 나아가면서 성장할 수 있습니다.'}, {'zodiac': '토끼띠', 'year': '1963', 'luck_msg': '가족과의 대화가 화목을 더합니다. 서로의 이야기를 나누며 이해해
 폭을 넓힐 수 있습니다.'}, {'zodiac': '토끼띠', 'year': '1975', 'luck_msg': '재정적인 계획을 세우는 것이 유리합니다. 지출을 관리하며 미래를 위한 준비를 하세요.'}, {'z z
odiac': '토끼띠', 'year': '1987', 'luck_msg': '자신의 감정을 잘 표현하면 대인관계가 좋아집니다. 솔직한 마음을 전달하면서 관계를 강화해보세요.'}, {'zodiac': '토끼띠', 'y
ear': '1999', 'luck_msg': '새로운 정보를 얻기에 좋은 날입니다. 관심 있는 분야의 지식을 넓히며 전문성을 키우세요.'}, {'zodiac': '용띠', 'year': '1964', 'luck_msg': '자신
을 가지고 도전하세요. 새로운 시도가 성공으로 이끌 수 있는 발판이 될 것입니다.'}, {'zodiac': '용띠', 'year': '1976', 'luck_msg': '가까운 사람과의 관계가 더욱 돈독해질   
것입니다. 서로를 위하는 마음이 소중한 추억을 만듭니다.'}, {'zodiac': '용띠', 'year': '1988', 'luck_msg': '긍정적인 사고방식이 중요한 하루입니다. 긍정의 힘으로 어려움을 
극복할 수 있습니다.'}, {'zodiac': '용띠', 'year': '2000', 'luck_msg': '학습이나 자기개발에 좋은 시간입니다. 새로운 지식을 습득하면서 미래를 위한 준비를 하세요.'}, {'zod
iac': '뱀띠', 'year': '1965', 'luck_msg': '주변 사람들에게 감사의 마음을 전하세요. 작은 감사가 인간관계를 더욱 풍요롭게 만듭니다.'}, {'zodiac': '뱀띠', 'year': '1977', 
'luck_msg': '오늘은 휴식을 취하는 것이 좋습니다. 충분한 휴식을 통해 내일을 위한 에너지를 충전하세요.'}, {'zodiac': '뱀띠', 'year': '1989', 'luck_msg': '작은 성취에도 만
을 느끼세요. 일상 속에서 작은 기쁨을 찾는 것이 중요합니다.'}, 

{'zodiac': '뱀띠', 'year': '2001', 'luck_msg': '새로운 환경에 적응하는 것이 중요합니다. 변화를 받아들이   
며 성장의 기회로 삼으세요.'}, {'zodiac': '말띠', 'year': '1966', 'luck_msg': '사랑하는 사람과의 대화가 중요합니다. 서로의 마음을 나누며 관계를 더욱 깊게 만들어보세요.'}
, {'zodiac': '말띠', 'year': '1978', 'luck_msg': '금전 관리에 신경을 쓰세요. 지출을 절제하며 재정 상태를 안정시키는 것이 중요합니다.'}, {'zodiac': '말띠', 'year': '1990
', 'luck_msg': '새로운 도전에 망설임 없이 나서보세요. 도전을 통해 자신의 한계를 넓힐 수 있습니다.'}, {'zodiac': '말띠', 'year': '2002', 'luck_msg': '목표를 세우고 체계 
적으로 준비하세요. 계획을 세워 차근차근 실천해 나가면 성공할 수 있습니다.'}, {'zodiac': '양띠', 'year': '1967', 'luck_msg': '가족과 함께하는 시간이 행복을 더합니다. 가 
족과의 대화를 통해 마음의 안정을 찾으세요.'}, {'zodiac': '양띠', 'year': '1979', 'luck_msg': '직장이나 학업에서 좋은 성과가 기대됩니다. 집중력을 발휘하면 놀라운 결과를 
얻을 수 있습니다.'}, {'zodiac': '양띠', 'year': '1991', 'luck_msg': '새로운 사람들과의 만남이 기쁨을 줍니다. 네트워킹을 통해 유용한 정보를 얻을 수 있습니다.'}, {'zodiac
': '양띠', 'year': '2003', 'luck_msg': '자신의 재능을 발휘할 기회가 있습니다. 자신감을 가지고 능력을 펼쳐보세요.'}, {'zodiac': '원숭이띠', 'year': '1956', 'luck_msg': '
오랜 친구와의 만남이 위로가 됩니다. 추억을 나누며 정서적 안정을 얻을 수 있습니다.'}, 

{'zodiac': '원숭이띠', 'year': '1968', 'luck_msg': '직장에서 긍정적인 변화가 기다리
 있습니다. 새로운 프로젝트나 업무가 기회가 될 수 있습니다.'}, {'zodiac': '원숭이띠', 'year': '1980', 'luck_msg': '주변 사람들과의 협력이 중요합니다. 함께하는 프로젝트트
서 좋은 결과를 얻을 수 있습니다.'}, {'zodiac': '원숭이띠', 'year': '1992', 'luck_msg': '건강에 조금 더 신경 쓰세요. 규칙적인 운동과 적절한 휴식이 필요한 시기입니다.'} }
, {'zodiac': '닭띠', 'year': '1957', 'luck_msg': '가족과의 대화가 풍요로운 관계를 만듭니다. 서로의 소통을 통해 가족 간의 유대를 강화하세요.'}, {'zodiac': '닭띠', 'year'
: '1969', 'luck_msg': '금전적인 이익을 얻을 수 있는 기회가 있습니다. 주의 깊게 기회를 포착하면 좋은 결과가 있을 것입니다.'}, {'zodiac': '닭띠', 'year': '1981', 'luck_ms
g': '새로운 활동이나 취미를 시작하기 좋은 날입니다. 새로운 도전을 통해 즐거움을 찾으세요.'}, {'zodiac': '닭띠', 'year': '1993', 'luck_msg': '친구들과의 대화에서 좋은 아
디어를 얻을 수 있습니다. 다양한 의견을 경청하는 것이 중요합니다.'}, 

{'zodiac': '개띠', 'year': '1958', 'luck_msg': '가족과의 관계가 더욱 돈독해질 것입니다. 서로의 소   
중함을 느끼며 함께 시간을 보내세요.'}, {'zodiac': '개띠', 'year': '1970', 'luck_msg': '새로운 목표를 설정하는 것이 유리합니다. 목표를 향해 나아가면서 성장할 수 있습니다
'}, {'zodiac': '개띠', 'year': '1982', 'luck_msg': '자신감을 가지고 도전하는 것이 좋습니다. 새로운 시도가 성공으로 이끌 수 있는 발판이 됩니다.'}, {'zodiac': '개띠', 'yy
ear': '1994', 'luck_msg': '긍정적인 사고방식이 중요한 하루입니다. 긍정의 힘으로 어려움을 극복할 수 있습니다.'}, {'zodiac': '돼지띠', 'year': '1959', 'luck_msg': '인간관
에서 좋은 소식이 있을 것입니다. 주변 사람들과의 소통을 통해 기쁨을 나누세요.'}, {'zodiac': '돼지띠', 'year': '1971', 'luck_msg': '재정적인 계획을 세우는 것이 유리합니니
. 지출을 관리하며 미래를 위한 준비를 하세요.'}, {'zodiac': '돼지띠', 'year': '1983', 'luck_msg': '사랑하는 사람과의 시간이 행복을 더합니다. 소중한 추억을 만들 수 있는는기회가 될 것입니다.'}, {'zodiac': '돼지띠', 'year': '1995', 'luck_msg': '새로운 정보를 얻기에 좋은 날입니다. 관심 있는 분야의 지식을 넓히며 전문성을 키우세요.'}
]} 
'''
'''
{'GptResponse': 
    [
        {
          "zodiac": "쥐띠",
          "year": "1960",
          "luck_msg": "새로운 만남이 기쁨을 가져다줄 것입니다. 소통의 장에서 빛을 발하게 될 것이니 자신감을 가지세요."
        },
        {
          "zodiac": "쥐띠",
          "year": "1972",
          "luck_msg": "주변 사람들과의 협력이 중요한 하루입니다. 함께 문제를 해결하면서 신뢰를 쌓을 수 있습니다."
        },
        {
          "zodiac": "쥐띠",
          "year": "1984",
          "luck_msg": "금전적인 이익을 얻을 좋은 기회가 있습니다. 세심한 주의를 기울이면 더 큰 성과를 기대할 수 있습니다."
        },
        {
          "zodiac": "쥐띠",
          "year": "1996",
          "luck_msg": "창의적인 아이디어가 많이 떠오를 것입니다. 이를 실현하기 위해 적극적으로 움직여 보세요."
        },
        {
          "zodiac": "소띠",
          "year": "1961",
          "luck_msg": "인내심을 가지고 차분하게 대응하면 문제가 해결됩니다. 급하게 서두르지 말고 여유를 가져보세요."
        },
        {
          "zodiac": "소띠",
          "year": "1973",
          "luck_msg": "가족과의 시간을 중요하게 생각해보세요. 소중한 추억을 만들 수 있는 기회가 될 것입니다."
        },
        {
          "zodiac": "소띠",
          "year": "1985",
          "luck_msg": "직장이나 학교에서 인정받을 일이 생길 것입니다. 노력한 만큼의 보상을 받게 될 것이니 자신감을 가져보세요."
        },
        {
          "zodiac": "소띠",
          "year": "1997",
          "luck_msg": "새로운 취미를 시작하는 것이 좋습니다. 새로운 활동을 통해 에너지를 얻을 수 있을 것입니다."
        },
        {
          "zodiac": "호랑이띠",
          "year": "1962",
          "luck_msg": "주변의 조언을 경청하는 것이 중요합니다. 다양한 의견을 수렴하면 좋은 결과로 이어질 것입니다."
        },
        {
          "zodiac": "호랑이띠",
          "year": "1974",
          "luck_msg": "건강에 조금 더 신경을 써야 할 때입니다. 규칙적인 운동과 충분한 휴식이 필요합니다."
        },
        {
          "zodiac": "호랑이띠",
          "year": "1986",
          "luck_msg": "친구들의 모임에서 즐거운 시간을 보낼 것입니다. 소통하며 에너지를 얻을 수 있습니다."
        },
        {
          "zodiac": "호랑이띠",
          "year": "1998",
          "luck_msg": "새로운 목표를 세우는 것이 좋습니다. 목표를 향해 한 걸음씩 나아가면서 성장할 수 있습니다."
        },
        {
          "zodiac": "토끼띠",
          "year": "1963",
          "luck_msg": "가족과의 대화가 화목을 더합니다. 서로의 이야기를 나누며 이해의 폭을 넓힐 수 있습니다."
        },
        {
          "zodiac": "토끼띠",
          "year": "1975",
          "luck_msg": "재정적인 계획을 세우는 것이 유리합니다. 지출을 관리하며 미래를 위한 준비를 하세요."
        },
        {
          "zodiac": "토끼띠",
          "year": "1987",
          "luck_msg": "자신의 감정을 잘 표현하면 대인관계가 좋아집니다. 솔직한 마음을 전달하면서 관계를 강화해보세요."
        },
        {
          "zodiac": "토끼띠",
          "year": "1999",
          "luck_msg": "새로운 정보를 얻기에 좋은 날입니다. 관심 있는 분야의 지식을 넓히며 전문성을 키우세요."
        },
        {
          "zodiac": "용띠",
          "year": "1964",
          "luck_msg": "자신을 가지고 도전하세요. 새로운 시도가 성공으로 이끌 수 있는 발판이 될 것입니다."
        },
        {
          "zodiac": "용띠",
          "year": "1976",
          "luck_msg": "가까운 사람과의 관계가 더욱 돈독해질 것입니다. 서로를 위하는 마음이 소중한 추억을 만듭니다."
        },
        {
          "zodiac": "용띠",
          "year": "1988",
          "luck_msg": "긍정적인 사고방식이 중요한 하루입니다. 긍정의 힘으로 어려움을 극복할 수 있습니다."
        },
        {
          "zodiac": "용띠",
          "year": "2000",
          "luck_msg": "학습이나 자기개발에 좋은 시간입니다. 새로운 지식을 습득하면서 미래를 위한 준비를 하세요."
        },
        {
          "zodiac": "뱀띠",
          "year": "1965",
          "luck_msg": "주변 사람들에게 감사의 마음을 전하세요. 작은 감사가 인간관계를 더욱 풍요롭게 만듭니다."
        },
        {
          "zodiac": "뱀띠",
          "year": "1977",
          "luck_msg": "오늘은 휴식을 취하는 것이 좋습니다. 충분한 휴식을 통해 내일을 위한 에너지를 충전하세요."
        },
        {
          "zodiac": "뱀띠",
          "year": "1989",
          "luck_msg": "작은 성취에도 만족을 느끼세요. 일상 속에서 작은 기쁨을 찾는 것이 중요합니다."
        },
        {
          "zodiac": "뱀띠",
          "year": "2001",
          "luck_msg": "새로운 환경에 적응하는 것이 중요합니다. 변화를 받아들이며 성장의 기회로 삼으세요."
        },
        {
          "zodiac": "말띠",
          "year": "1966",
          "luck_msg": "사랑하는 사람과의 대화가 중요합니다. 서로의 마음을 나누며 관계를 더욱 깊게 만들어보세요."
        },
        {
          "zodiac": "말띠",
          "year": "1978",
          "luck_msg": "금전 관리에 신경을 쓰세요. 지출을 절제하며 재정 상태를 안정시키는 것이 중요합니다."
        },
        {
          "zodiac": "말띠",
          "year": "1990",
          "luck_msg": "새로운 도전에 망설임 없이 나서보세요. 도전을 통해 자신의 한계를 넓힐 수 있습니다."
        },
        {
          "zodiac": "말띠",
          "year": "2002",
          "luck_msg": "목표를 세우고 체계적으로 준비하세요. 계획을 세워 차근차근 실천해 나가면 성공할 수 있습니다."
        },
        {
          "zodiac": "양띠",
          "year": "1967",
          "luck_msg": "가족과 함께하는 시간이 행복을 더합니다. 가족과의 대화를 통해 마음의 안정을 찾으세요."
        },
        {
          "zodiac": "양띠",
          "year": "1979",
          "luck_msg": "직장이나 학업에서 좋은 성과가 기대됩니다. 집중력을 발휘하면 놀라운 결과를 얻을 수 있습니다."
        },
        {
          "zodiac": "양띠",
          "year": "1991",
          "luck_msg": "새로운 사람들과의 만남이 기쁨을 줍니다. 네트워킹을 통해 유용한 정보를 얻을 수 있습니다."
        },
        {
          "zodiac": "양띠",
          "year": "2003",
          "luck_msg": "자신의 재능을 발휘할 기회가 있습니다. 자신감을 가지고 능력을 펼쳐보세요."
        },
        {
          "zodiac": "원숭이띠",
          "year": "1956",
          "luck_msg": "오랜 친구와의 만남이 위로가 됩니다. 추억을 나누며 정서적 안정을 얻을 수 있습니다."
        },
        {
          "zodiac": "원숭이띠",
          "year": "1968",
          "luck_msg": "직장에서 긍정적인 변화가 기다리고 있습니다. 새로운 프로젝트나 업무가 기회가 될 수 있습니다."
        },
        {
          "zodiac": "원숭이띠",
          "year": "1980",
          "luck_msg": "주변 사람들과의 협력이 중요합니다. 함께하는 프로젝트에서 좋은 결과를 얻을 수 있습니다."
        },
        {
          "zodiac": "원숭이띠",
          "year": "1992",
          "luck_msg": "건강에 조금 더 신경 쓰세요. 규칙적인 운동과 적절한 휴식이 필요한 시기입니다."
        },
        {
          "zodiac": "닭띠",
          "year": "1957",
          "luck_msg": "가족과의 대화가 풍요로운 관계를 만듭니다. 서로의 소통을 통해 가족 간의 유대를 강화하세요."
        },
        {
          "zodiac": "닭띠",
          "year": "1969",
          "luck_msg": "금전적인 이익을 얻을 수 있는 기회가 있습니다. 주의 깊게 기회를 포착하면 좋은 결과가 있을 것입니다."
        },
        {
          "zodiac": "닭띠",
          "year": "1981",
          "luck_msg": "새로운 활동이나 취미를 시작하기 좋은 날입니다. 새로운 도전을 통해 즐거움을 찾으세요."
        },
        {
          "zodiac": "닭띠",
          "year": "1993",
          "luck_msg": "친구들과의 대화에서 좋은 아이디어를 얻을 수 있습니다. 다양한 의견을 경청하는 것이 중요합니다."
        },
        {
          "zodiac": "개띠",
          "year": "1958",
          "luck_msg": "가족과의 관계가 더욱 돈독해질 것입니다. 서로의 소중함을 느끼며 함께 시간을 보내세요."
        },
        {
          "zodiac": "개띠",
          "year": "1970",
          "luck_msg": "새로운 목표를 설정하는 것이 유리합니다. 목표를 향해 나아가면서 성장할 수 있습니다."
        },
        {
          "zodiac": "개띠",
          "year": "1982",
          "luck_msg": "자신감을 가지고 도전하는 것이 좋습니다. 새로운 시도가 성공으로 이끌 수 있는 발판이 됩니다."
        },
        {
          "zodiac": "개띠",
          "year": "1994",
          "luck_msg": "긍정적인 사고방식이 중요한 하루입니다. 긍정의 힘으로 어려움을 극복할 수 있습니다."
        },
        {
          "zodiac": "돼지띠",
          "year": "1959",
          "luck_msg": "인간관계에서 좋은 소식이 있을 것입니다. 주변 사람들과의 소통을 통해 기쁨을 나누세요."
        },
        {
          "zodiac": "돼지띠",
          "year": "1971",
          "luck_msg": "재정적인 계획을 세우는 것이 유리합니다. 지출을 관리하며 미래를 위한 준비를 하세요."
        },
        {
          "zodiac": "돼지띠",
          "year": "1983",
          "luck_msg": "사랑하는 사람과의 시간이 행복을 더합니다. 소중한 추억을 만들 수 있는 기회가 될 것입니다."
        },
        {
          "zodiac": "돼지띠",
          "year": "1995",
          "luck_msg": "새로운 정보를 얻기에 좋은 날입니다. 관심 있는 분야의 지식을 넓히며 전문성을 키우세요."
        }
    ]
}
    
'''