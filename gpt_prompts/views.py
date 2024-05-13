from datetime import datetime, timedelta
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from drf_spectacular.utils import extend_schema, OpenApiExample
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

    @extend_schema(tags=['PromptMsg'],
                   description="BE-GPT101(GET): 오늘의 한마디에 사용되는 최신(마지막 gpt_id) 프롬프트 메세지 로드"
    )
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
    @extend_schema(tags=['PromptMsg'],
        examples=[
            OpenApiExample(
                'Example',
                value={'prompt_msg' : "GPT야 오늘의 한마디 알려줘"
                },
                request_only=True,  # 요청 본문에서만 예시 사용
            )
        ],
        description="BE-GPT102(POST): 오늘의 한마디에 사용되는 최신(마지막 gpt_id) 프롬프트 메세지 저장"
    )
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

    @extend_schema(tags=['PromptMsg'],
                   description="BE-GPT201(GET): 띠별 운세에 사용되는 최신(마지막 gpt_id) 프롬프트 메세지 로드"
    )
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
    @extend_schema(tags=['PromptMsg'],
        examples=[
            OpenApiExample(
                'Example',
                value={'prompt_msg' : "GPT야 띠별 운세를 알려줘"
                },
                request_only=True,  # 요청 본문에서만 예시 사용
            )
        ],
        description="BE-GPT202(POST): 띠별 운세에 사용되는 최신(마지막 gpt_id) 프롬프트 메세지 저장"
    )
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

    @extend_schema(tags=['PromptMsg'],
        description="BE-GPT301(GET): 별자리별 운세에 사용되는 최신(마지막 gpt_id) 프롬프트 메세지 로드"
    )
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
    @extend_schema(tags=['PromptMsg'],
        examples=[
            OpenApiExample(
                'Example',
                value={'prompt_msg' : "GPT야 별자리별 운세 알려줘"
                },
                request_only=True,  # 요청 본문에서만 예시 사용
            )
        ],
        description="BE-GPT302(POST): 별자리별 운세에 사용되는 최신(마지막 gpt_id) 프롬프트 메세지 저장"
    )
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

    @extend_schema(tags=['PromptMsg'],
                   description="BE-GPT401(GET): MBTI별 운세에 사용되는 최신(마지막 gpt_id) 프롬프트 메세지 로드"
    )
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
    @extend_schema(tags=['PromptMsg'],
        examples=[
            OpenApiExample(
                'Example',
                value={'prompt_msg' : "GPT야 MBTI별 운세 알려줘"
                },
                request_only=True,  # 요청 본문에서만 예시 사용
            )
        ],
        description="BE-GPT402(POST): MBTI별 운세에 사용되는 최신(마지막 gpt_id) 프롬프트 메세지 저장"
    )
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


#프롬프트 메세지를 사용해서 GPT에게 별자리 운세 받기
# api/v1/prompt/gpt-star
class GptStar(APIView):
    #스웨거를 위한 시리얼라이저 설정
    serializer_class = PromptLuckSerializer
    #스웨거 API구분을 위한 데코레이터
    @extend_schema(tags=['GPT'],
        examples=[
            OpenApiExample(
                'Example',
                value={'category': "star"
                },
                request_only=True,  # 요청 본문에서만 예시 사용
            )
        ],
        description="category가 star인 프롬프트중에서 가장 최근의 프롬프트메세지를 사용하여 GPT에 운세 생성요청하여 결과를 DB에 저장"
    )
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
            prompt = PromptGptApiSerializer(prompt_msg).data['prompt_msg']
            prompt = prompt

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
        #             'star': '물병자리',
        #             'date_range': '01/20~02/18',
        #             'luck_msg': '새로운 아이디어가 떠오르는 날입니다. 창의적인 접근을 시도해 보세요. 인간관계에서도 긍정적인 에너지가 흐릅니다.'
        #         },
        #         {
        #             'star': '물고기자리',
        #             'date_range': '02/19~03/20',
        #             'luck_msg': '감성이 풍부해지는 하루가 예상됩니다. 주변 사람들과의 대화에서 위로를 받을 거요. 예술적인 활동에 참여해 보세요.'
        #         },
        #         {
        #             'star': '양자리',
        #             'date_range': '03/21~04/19',
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
                    'attribute1': msg['star'],
                    'attribute2': msg['date_range'],
                    'luck_msg' :  msg['luck_msg']
                })


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


#프롬프트 메세지를 사용해서 GPT에게 별자리 운세 받기
# api/v1/prompt/gpt-mbti
class GptMBTI(APIView):
    #스웨거를 위한 시리얼라이저 설정
    serializer_class = PromptLuckSerializer
    #스웨거 API구분을 위한 데코레이터
    @extend_schema(tags=['GPT'],
        examples=[
            OpenApiExample(
                'Example',
                value={'category': "MBTI"
                },
                request_only=True,  # 요청 본문에서만 예시 사용
            )
        ],
        description="category가 MBTI인 프롬프트중에서 가장 최근의 프롬프트메세지를 사용하여 GPT에 운세 생성요청하여 결과를 DB에 저장"
    )
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
            prompt = PromptGptApiSerializer(prompt_msg).data['prompt_msg']
            prompt = prompt

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
        #             'MBTI': 'ENTP',
        #             'luck_msg': '감성이 풍부해지는 하루가 예상됩니다. 주변 사람들과의 대화에서 위로를 받을 거요. 예술적인 활동에 참여해 보세요.'
        #         },
        #         {
        #             'MBTI': 'INFJ',
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
                    'attribute1': msg['MBTI'],
                    'luck_msg' :  msg['luck_msg']
                })


            if gpt_msg:
                for msg in gpt_msg:
                    serializer = PromptLuckSerializer(data={
                        'luck_date' : luck_date,
                        'category' : category,
                        'attribute1' : msg['attribute1'],
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