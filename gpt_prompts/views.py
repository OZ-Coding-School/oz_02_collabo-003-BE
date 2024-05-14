import json
from openai import OpenAI
from datetime import datetime, timedelta
from drf_spectacular.utils import extend_schema, OpenApiExample
from drf_spectacular.utils import extend_schema, OpenApiExample
from rest_framework import status
from rest_framework.exceptions import ParseError
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.paginator import Paginator # pagination
from kluck_env import env_settings as env
from luck_messages.serializers import *
from .serializers import *
from .models import GptPrompt


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
                value={'prompt_msg' : "오늘의 한마디를 총 3개를 작성할거야. 아침에 하루를 시작하는 사람들이 이 글을보고 힘이나고 위로를 받았으면 해. 작성 방법은 예시를 참고해줘. 예시 '꽃비 내리는 날 설레이는 봄이에요.🌟 꽃 향기처럼 부드럽고 향기로운 하루 보내시길 바래요.🌈 당신의 편에 서서 응원할게요!💪' 과하게 부정적인 내용, 성적인 내용, 추상적인 내용은 피해줘. 내용 작성 시  '오늘', '오늘은' 이라는 단어는 제외하고 어투는 너무 딱딱하지 않고 부드러우면서도 반말은 사용하지 말고 존댓말을 사용해. 문장 가운데마다 이모티콘을 적절히 2개 이상 4개 미만으로 넣어서 작성해줘. 내용 길이를  45자 이상 50자 미만으로 작성해주고, 2문장으로 작성해줘."},
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
                value={'prompt_msg' : "띠별 운세를 작성할꺼야. 작성해야하는 대상자는 1956년 부터 2003년에 태어난 사람이야. 가장 큰 제목은 띠이고, 세부항목은 태어난 연도이고 해당되는 연도를 각각 나눠서 작성해야해. 작성 방법은 예시를 참고해줘. 예시: '원숭이 1968 직장에서 긍정적인 변화가 기다리고 있습니다. 새로운 프로젝트나 업무가 기회가 될 수 있습니다. 적극적인 태도가 중요합니다.' 과하게 부정적인 내용, 성적인 내용, 추상적인 내용은 피해줘. 내용 작성 시  '오늘 ~년생'이라는 말은 제외하고 어투는 너무 딱딱하지 않고 부드러우면서도 반말은 사용하지 말고 존댓말을 사용해줘. 각각의 운세 내용 길이를 60자 이상 65자 미만으로 충분히 길게 작성해주고, 3문장으로 작성해줘."
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
                value={'prompt_msg' : "별자리별 운세를 작성할꺼야. '물병자리 (01/20~02/18)', '물고기자리 (02/19~03/20)', '양자리 (03/21~04/19)', '황소자리 (04/20~05/20)', '쌍둥이자리 (05/21~06/20)', '게자리 (06/21~07/22)', '사자자리 (07/23~08/22)', '처녀자리 (08/23~09/22)', '천칭자리 (09/23~10/22)', '전갈자리 (10/23~11/21)', '사수자리 (11/22~12/21)', '염소자리 (12/22~01/19)' 총 12개의 별자리이고 작성방법은 예시를 참고해줘. 예시:'물병자리 (01/20~02/18) 오늘은 어디를 가서도 당신의 밥그릇은 챙길 수 있는 날입니다. 되도록 마음을 크게 먹는 것이 좋습니다. 쪼잔 하다는 소리를 듣지 않도록 조심하세요. 당신의 마음 수양이 제대로 이루어질수록 행운이 따릅니다.' 과하게 부정적인 내용, 성적인 내용, 추상적인 내용은 피해줘. 내용 작성 시 '오늘 ~별자리'이라는 말은 제외하고 어투는 너무 딱딱하지 않고 부드러우면서도 반말은 사용하지 말고 존댓말을 사용해. 각각의 운세 내용 길이를 60자 이상 65자 미만으로 충분히 길게 작성해주고, 3문장으로 작성해줘."
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
                value={'prompt_msg' : "작성해야하는 MBTI 유형이야. ISTJ, ISFJ, INFJ, INTJ, ISTP, ISFP, INFP, INTP, ESTP, ESFP, ENFP, ENTP, ESTJ, ESFJ, ENFJ, ENTJ 총 16개의 MBTI 각 유형별로 작성해줘. 작성 방법은 예시를 참고해줘. 예시'ISTJ 오늘은 당신에게 청정한 감성과 정확성이 빛나는 하루가 될 것입니다. 일에 대한 책임감을 가지고 차분하게 일 처리를 하면 좋은 결과를 얻을 수 있을 것입니다.' 과하게 부정적인 내용, 성적인 내용, 추상적인 내용은 피해줘. 내용 작성 시 '오늘은'이라는 말은 제외하고 어투는 너무 딱딱하지 않고 부드러우면서도 반말은 사용하지 말고 존댓말을 사용해. 각각의 운세 내용 길이를 60자 이상 65자 미만으로 충분히 길게 작성해주고,  3문장으로 작성해."
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


# 각 유형별 운세 프롬프트 히스토리
# api/v1/prompt/<str:category>/history
class PromptHistory(APIView):
    '''
    BE-GPT103(203, 303, 403): 입력받는 카테고리에 해당하는 프롬프트 메세지 전체 로드
    '''
    serializer_class = PromptHistorySerializer

    @extend_schema(tags=['PromptMsg'])
    def get(self, request, category, page):
        try:
            prompt_msgs = GptPrompt.objects.filter(category=category)
            paginator = Paginator(prompt_msgs, 4) # 페이지당 4개의 객체를 보여줍니다. 개수는 원하는대로 조정하세요.

            page_obj = paginator.get_page(page)

            serializer = PromptHistorySerializer(page_obj, many=True)
            return Response({
                'total': prompt_msgs.count(), # 총 데이터 개수
                'prompt_msgs': serializer.data, # 페이지네이션된 데이터
            }, status=status.HTTP_200_OK)
        except GptPrompt.DoesNotExist:
            return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)


# GPT API 사용
# 1. 오늘의 한마디 받기.
# /api/v1/gpt/today/
class GptToday(APIView):
    #스웨거를 위한 시리얼라이저 설정
    serializer_class = TodaySerializer
    
    #스웨거 API구분을 위한 데코레이터
    @extend_schema(tags=['GPT !!BD팀, FE팀에서는 사용하지 말아주세요. BE전용입니다.!!'],
        examples=[
            OpenApiExample(
                'Example',
                value={'입력값 없음'
                },
                request_only=True,  # 요청 본문에서만 예시 사용
            )
        ],
        description="category가 today인 프롬프트중에서 가장 최근의 프롬프트메세지를 사용하여 GPT에 운세 생성요청하여 결과를 DB에 저장"
    )

    def post(self, request):
        # GPT API Key 설정
        api_key = env.API_KEY
        gpt_client = OpenAI(api_key=api_key)

        # post 요청의 카테고리로 관련 최근 프롬프트메세지 로드
        category = 'today'
        today_prompt = GptPrompt.objects.filter(category=category).order_by('-gpt_id').first()

        # 프롬프트 메세지 여부 확인
        if today_prompt:
            # now = datetime.now()
            a_week = datetime.now() + timedelta(days=7)
            luck_date = a_week.strftime('%Y%m%d')
            gpt_id = PromptHistorySerializer(today_prompt).data['gpt_id']
            prefix_prompt = '{"GptResponse":[{"message_num": "1", "luck_msg": "메세지"}, ...]}예시와 같은 json 형식으로 작성해줘.'
            prompt_date = luck_date[:4] +'년'+ luck_date[4:6] + '월' + luck_date[6:] + '일 '
            prompt = PromptHistorySerializer(today_prompt).data['prompt_msg']
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

            today_data = json.loads(response.choices[0].message.content)
        else:
            return Response(status=status.HTTP_402_PAYMENT_REQUIRED)

        # today_data 예시
        # today_data = dict(
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

        if today_data:
            # 메세지 처리용 리스트
            today_msg = []

            # DB컬럼에 맞게 dict로 변경
            for msg in today_data['GptResponse']:
                today_msg.append({
                    'attribute2': msg['message_num'],
                    'luck_msg' :  msg['luck_msg']
                })


            if today_msg:
                for msg in today_msg:
                    serializer = TodaySerializer(data={
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


# 2. 띠별 운세 받기.
# /api/v1/gpt/zodiac/
class GptZodiac(APIView):
    #스웨거를 위한 시리얼라이저 설정
    serializer_class = ZodiacSerializer
    
    #스웨거 API 구분을 위한 데코레이터
    @extend_schema(tags=['GPT !!BD팀, FE팀에서는 사용하지 말아주세요. BE전용입니다.!!'],
        examples=[
            OpenApiExample(
                'Example',
                value={'입력값없음.'
                },
                request_only=True,  # 요청 본문에서만 예시 사용
            )
        ],
        description="category가 zodiac인 프롬프트중에서 가장 최근의 프롬프트메세지를 사용하여 GPT에 운세 생성요청하여 결과를 DB에 저장"
    )

    def post(self, request):
        # GPT API Key 설정
        api_key = env.API_KEY
        gpt_client = OpenAI(api_key=api_key)

        # post 요청의 카테고리로 관련 최근 프롬프트메세지 로드
        category = 'zodiac'
        zodiac_prompt = GptPrompt.objects.filter(category=category).order_by('-gpt_id').first()


        # 프롬프트 메세지 여부 확인
        if zodiac_prompt:
            # now = datetime.now()
            a_week = datetime.now() + timedelta(days=7)
            luck_date = a_week.strftime('%Y%m%d')
            gpt_id = PromptHistorySerializer(zodiac_prompt).data['gpt_id']
            prefix_prompt = '{"GptResponse":[{"zodiac": "닭", "year": "1981", "luck_msg": "메세지"}, ...]}예시와 같은 json 형식으로 작성해줘.'
            prompt_date = luck_date[:4] +'년'+ luck_date[4:6] + '월' + luck_date[6:] + '일 '
            # GPT가 너무 긴 답변을 처리하지 못해서 2파트로 나눠서 요청을 보냄.
            suffix_prompt1 = '12간지 중에서 쥐, 소, 호랑이, 토끼, 용, 뱀을 작성해줘'
            suffix_prompt2 = '12간지 중에서 말, 양, 원숭이, 닭, 개, 돼지을 작성해줘'
            prompt = PromptHistorySerializer(zodiac_prompt).data['prompt_msg']

            # GPT에게 보낼 질문 메세지
            prompts = []
            prompts.append(prefix_prompt + prompt_date + prompt + suffix_prompt1)
            prompts.append(prefix_prompt + prompt_date + prompt + suffix_prompt2)

            # 메세지 처리용 리스트
            zodiac_msg = []

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

                zodiac_data = json.loads(response.choices[0].message.content)

                # zodiac_data 예시
                # zodiac_data = dict(
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

                if zodiac_data:
                    # DB컬럼에 맞게 dict로 변경
                    for msg in zodiac_data['GptResponse']:
                        zodiac_msg.append({
                            'attribute1': msg['zodiac'],
                            'attribute2': msg['year'],
                            'luck_msg' :  msg['luck_msg']
                        })

        else:
            return Response(status=status.HTTP_402_PAYMENT_REQUIRED)

        # GPT에 요청 결과를 DB에 넣기
        if zodiac_msg:
            for msg in zodiac_msg:
                serializer = ZodiacSerializer(data={
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


# 3. 별자리 운세 받기.
# api/v1/prompt/gpt-star
class GptStar(APIView):
    #스웨거를 위한 시리얼라이저 설정
    serializer_class = StarSerializer
    
    #스웨거 API 구분을 위한 데코레이터
    @extend_schema(tags=['GPT !!BD팀, FE팀에서는 사용하지 말아주세요. BE전용입니다.!!'],
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
        # GPT API Key 설정
        api_key = env.API_KEY
        gpt_client = OpenAI(api_key=api_key)

        # post 요청의 카테고리로 관련 최근 프롬프트메세지 로드
        category = 'star'
        star_prompt = GptPrompt.objects.filter(category=category).order_by('-gpt_id').first()

        # 프롬프트 메세지 여부 확인
        if star_prompt:
            a_week = datetime.now() + timedelta(days=7)
            luck_date = a_week.strftime('%Y%m%d')
            gpt_id = PromptHistorySerializer(star_prompt).data['gpt_id']
            prompt = PromptHistorySerializer(star_prompt).data['prompt_msg']
            prefix_prompt = '{"GptResponse":[{"star": "물병자리", "date_range": "01/20~02/18", "luck_msg": "메세지"}, ...]}예시와 같은 json 형식으로 작성해줘.'
            prompt_date = luck_date[:4] +'년'+ luck_date[4:6] + '월' + luck_date[6:] + '일 '
            prompt = PromptHistorySerializer(star_prompt).data['prompt_msg']
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

            star_data = json.loads(response.choices[0].message.content)

        else:
            return Response(status=status.HTTP_402_PAYMENT_REQUIRED)

        # star_data 예시
        # star_data = dict(
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

        if star_data:
            # 메세지 처리용 리스트
            star_msg = []

            # DB컬럼에 맞게 dict로 변경
            for msg in star_data['GptResponse']:
                star_msg.append({
                    'attribute1': msg['star'],
                    'attribute2': msg['date_range'],
                    'luck_msg' :  msg['luck_msg']
                })

            if star_msg:
                for msg in star_msg:
                    serializer = StarSerializer(data={
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


# 4. MBTI 운세 받기
# api/v1/gpt/mbti/
class GptMbti(APIView):
    #스웨거를 위한 시리얼라이저 설정
    serializer_class = MbtiSerializer
    
    #스웨거 API구분을 위한 데코레이터
    @extend_schema(tags=['GPT !!BD팀, FE팀에서는 사용하지 말아주세요. BE전용입니다.!!'],
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
        # GPT API Key 설정
        api_key = env.API_KEY
        gpt_client = OpenAI(api_key=api_key)

        # post 요청의 카테고리로 관련 최근 프롬프트메세지 로드
        category = 'MBTI'
        mbti_prompt = GptPrompt.objects.filter(category=category).order_by('-gpt_id').first()

        # 프롬프트 메세지 여부 확인
        if mbti_prompt:
            # now = datetime.now()
            a_week = datetime.now() + timedelta(days=7)
            luck_date = a_week.strftime('%Y%m%d')
            gpt_id = PromptHistorySerializer(mbti_prompt).data['gpt_id']
            prompt = PromptHistorySerializer(mbti_prompt).data['prompt_msg']
            prefix_prompt = '{"GptResponse":[{"MBTI": "ENTP", "luck_msg": "메세지"}, ...]}예시와 같은 json 형식으로 작성해줘.'
            prompt_date = luck_date[:4] +'년'+ luck_date[4:6] + '월' + luck_date[6:] + '일 '
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

            mbti_data = json.loads(response.choices[0].message.content)
            
        else:
            return Response(status=status.HTTP_402_PAYMENT_REQUIRED)
        
        # mbti_data 예시
        # mbti_data = dict(
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

        if mbti_data:
            # 메세지 처리용 리스트
            mbti_msg = []

            # DB컬럼에 맞게 dict로 변경
            for msg in mbti_data['GptResponse']:
                mbti_msg.append({
                    'attribute1': msg['MBTI'],
                    'luck_msg' :  msg['luck_msg']
                })

            if mbti_msg:
                for msg in mbti_msg:
                    serializer = StarSerializer(data={
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