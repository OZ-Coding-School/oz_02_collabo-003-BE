import json
from openai import OpenAI
from datetime import datetime, timedelta
from drf_spectacular.utils import extend_schema, OpenApiExample
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from rest_framework_simplejwt.tokens import AccessToken # 엑세스토큰 임포트
from django.core.paginator import Paginator # pagination
from django.shortcuts import get_object_or_404
from kluck_env import env_settings as env
from luck_messages.serializers import *
from luck_messages.models import LuckMessage
from .serializers import *
from .models import GptPrompt
from admins.models import kluck_Admin
from admin_settings.models import AdminSetting


# 각 카테고리별 프롬프트 조회 및 생성
# api/v1/prompt/{category}/
class PromptIndividual(APIView):
    '''
    BE-GPT101, 201, 301, 401(GET): 카테고리별 사용되는 최신(마지막 gpt_id) 프롬프트 메세지 로드\n
    BE-GPT102, 202, 302, 402(POST): 카테고리별 사용되는 최신(마지막 gpt_id) 프롬프트 메세지 저장
    '''
    serializer_class = PromptSerializer

    # 프롬프트 메세지 최신 1개 조회
    @extend_schema(tags=['PromptMsg'],
                    description="BE-GPT101, 201, 301, 401(GET): 카테고리별 사용되는 최신(마지막 gpt_id) 프롬프트 메세지 로드"
    )
    def get(self, request, category):
        # 업데이트하는 방식 X, 프롬프트 메세지 이름 사용 X
        try:
            latest_today = GptPrompt.objects.filter(category=category).order_by('-gpt_id').first()
            serializer = PromptSerializer(latest_today)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except GptPrompt.DoesNotExist:
            return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

    # 프롬프트 메세지 수정 - 추가하는 방식
    @extend_schema(tags=['PromptMsg'],
        examples=[
            OpenApiExample(
                'Example - category: today',
                value={
                    'prompt_msg' : "오늘의 한마디를 하나 작성할 거야. 아침에 하루를 시작하는 사람들이 이 글을 보고 힘이 나고 위로를 받았으면 해. 작성 방법은 예시를 참고해 줘. 예시 '꽃비 내리는 날 설레는 봄이에요.🌟 꽃 향기처럼 부드럽고 향기로운 하루 보내시길 바라요.🌈 당신의 편에 서서 응원할게요!💪' 과하게 부정적인 내용, 성적인 내용, 추상적인 내용은 피해줘. 내용 작성 시 '오늘', '오늘은' 이라는 단어는 제외하고 어투는 너무 딱딱하지 않고 부드러우면서도 반말은 사용하지 말고 존댓말을 사용해. 문장 가운데마다 이모티콘을 적절히 2개 이상 4개 미만으로 넣어서 작성해 줘. 내용 길이를 45자 이상 50자 미만으로 작성해 주고, 2문장으로 작성해 줘."
                },
                request_only=True,  # 요청 본문에서만 예시 사용
            ),
            OpenApiExample(
                'Example - category: zodiac',
                value={
                    'prompt_msg' : "띠별 운세를 작성할 거야. 작성해야 하는 대상자는 1960년부터 2007년에 태어난 사람이야. 가장 큰 제목은 띠이고, 세부 항목은 태어난 연도이고 해당하는 연도를 각각 나눠서 작성해야 해. 작성 방법은 예시를 참고해 줘. 예시: '원숭이 1968 직장에서 긍정적인 변화가 기다리고 있습니다. 새로운 프로젝트나 업무가 기회가 될 수 있습니다. 적극적인 태도가 중요합니다.' 과하게 부정적인 내용, 성적인 내용, 추상적인 내용은 피해줘. 내용 작성 시 '오늘 ~년생'이라는 말은 제외하고 어투는 너무 딱딱하지 않고 부드러우면서도 반말은 사용하지 말고 존댓말을 사용해 줘. 각각의 운세 내용 길이를 한글로 무조건 공백 포함 65자 미만으로 작성해 줘. 3문장으로 작성해 줘."
                },
                request_only=True,  # 요청 본문에서만 예시 사용
            ),
            OpenApiExample(
                'Example - category: star',
                value={
                    'prompt_msg' : "별자리별 운세를 작성할꺼야. '물병자리 (01/20~02/18)', '물고기자리 (02/19~03/20)', '양자리 (03/21~04/19)', '황소자리 (04/20~05/20)', '쌍둥이자리 (05/21~06/21)', '게자리 (06/22~07/22)', '사자자리 (07/23~08/22)', '처녀자리 (08/23~09/22)', '천칭자리 (09/23~10/22)', '전갈자리 (10/23~11/21)', '궁수자리 (11/22~12/21)', '염소자리 (12/22~01/19)' 총 12개의 별자리이고 작성방법은 예시를 참고해줘. 예시:'물병자리 (01/20~02/18) 오늘은 어디를 가서도 당신의 밥그릇은 챙길 수 있는 날입니다. 되도록 마음을 크게 먹는 것이 좋습니다. 쪼잔 하다는 소리를 듣지 않도록 조심하세요. 당신의 마음 수양이 제대로 이루어질수록 행운이 따릅니다.' 과하게 부정적인 내용, 성적인 내용, 추상적인 내용은 피해줘. 내용 작성 시 '오늘 ~별자리'이라는 말은 제외하고 어투는 너무 딱딱하지 않고 부드러우면서도 반말은 사용하지 말고 존댓말을 사용해. 각각의 운세 내용 길이를 60자 이상 65자 미만으로 충분히 길게 작성해주고, 3문장으로 작성해줘."
                },
                request_only=True,  # 요청 본문에서만 예시 사용
            ),
            OpenApiExample(
                'Example - category: mbti',
                value={
                    'prompt_msg' : "작성해야하는 MBTI 유형이야. ISTJ, ISFJ, INFJ, INTJ, ISTP, ISFP, INFP, INTP, ESTP, ESFP, ENFP, ENTP, ESTJ, ESFJ, ENFJ, ENTJ 총 16개의 MBTI 각 유형별로 작성해줘. 작성 방법은 예시를 참고해줘. 예시'ISTJ 오늘은 당신에게 청정한 감성과 정확성이 빛나는 하루가 될 것입니다. 일에 대한 책임감을 가지고 차분하게 일 처리를 하면 좋은 결과를 얻을 수 있을 것입니다.' 과하게 부정적인 내용, 성적인 내용, 추상적인 내용은 피해줘. 내용 작성 시 '오늘은'이라는 말은 제외하고 어투는 너무 딱딱하지 않고 부드러우면서도 반말은 사용하지 말고 존댓말을 사용해. 각각의 운세 내용 길이를 60자 이상 65자 미만으로 충분히 길게 작성해주고,  3문장으로 작성해."
                },
                request_only=True,  # 요청 본문에서만 예시 사용
            )
        ],
        description="BE-GPT102, 202, 302, 402(POST): 카테고리별 사용되는 최신(마지막 gpt_id) 프롬프트 메세지 저장"
    )
    def post(self, request, category):
        # 토큰으로 인증 된 관리자의 user_id 확인
        # 헤더에서 인증관련 값 추출
        auth_header = request.headers.get('authorization')
        # 인증관련 내용에서 Bearer를 제외한 실제 토큰 추출
        token = auth_header.split(" ")[1]
        # 토큰에서 user_id추출
        # 엑세스토큰 디코드
        decoded_token = AccessToken(token)
        # user_id를 포함안 kluck_admin instance
        kluck_admin_user_id = kluck_Admin.objects.get(user_id = decoded_token.payload.get('user_id'))

        now = datetime.now()
        today = now.strftime('%Y%m%d')

        # 토큰에서 확인한 user_id
        user_id = decoded_token.payload.get('user_id')
        # 리퀘스트에 user_id 키, 값 추가
        request.data['user_id'] = user_id

        serializer = PromptSerializer(data=request.data)
        
        # admin_settings에 있는 term_date 값 가져오기.
        term = get_object_or_404(AdminSetting).term_date
        # last = now + timedelta(days=int(term))


        if serializer.is_valid():
            create_date = today
            # last_date = last.strftime('%Y%m%d')

            serializer.save(category=category, create_date=create_date, user_id=kluck_admin_user_id)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)


# 각 카테고리별 운세 프롬프트 히스토리
# api/v1/prompt/<str:category>/history
class PromptHistory(APIView):
    '''
    BE-GPT103(203, 303, 403): 입력받는 카테고리에 해당하는 프롬프트 메세지 전체 로드
    '''
    serializer_class = PromptHistorySerializer

    @extend_schema(tags=['PromptMsg'])
    def get(self, request, category, page):
        try:
            prompt_msgs = GptPrompt.objects.filter(category=category).order_by('-gpt_id')
            paginator = Paginator(prompt_msgs, 4) # 페이지당 4개의 객체를 보여줍니다. 개수는 원하는대로 조정하세요.

            page_obj = paginator.get_page(page)

            serializer = PromptHistorySerializer(page_obj, many=True)
            return Response({
                'total': prompt_msgs.count(), # 총 데이터 개수
                'prompt_msgs': serializer.data, # 페이지네이션된 데이터
            }, status=status.HTTP_200_OK)
        except GptPrompt.DoesNotExist:
            return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)


# # 운세 데이터 성공 여부를 위한 변수 설정.
# success_count = 0

# 각 API 요청별 운세 받기 함수의 success_count 더하기 함수.
def run_gpt_functions(luck_date):
    success_count = 0
    if GptToday(luck_date):
        success_count += 1
    if GptStar(luck_date):
        success_count += 2
    if GptMbti(luck_date):
        success_count += 4
    if GptZodiac1(luck_date):
        success_count += 8
    if GptZodiac2(luck_date):
        success_count += 16
    return success_count

# 운세 작업 진행도를 확인하기 위한 함수들
# 1. 운세 작업 상태 확인 데이터 생성 함수
def add_work_date(luck_date):
    work_serializer = TodaySerializer(data={
        'luck_date' : luck_date,
        'category' : 'work',
        'attribute2' : 0,
        'gpt_id' : 1,
    })

    if work_serializer.is_valid():
        work_serializer.save()
        return True
    else:
        log_error(work_serializer.errors)
        return False
    
# 2. 운세 작업 상태 확인 데이터 업데이트 함수
def update_work_date(worked):
    work_again_serializer = TodaySerializer(worked, data={'attribute2' : 0, 'gpt_id' : 1}, partial=True)
    if work_again_serializer.is_valid():
        work_again_serializer.save()
        return True
    else:
        log_error(work_again_serializer.errors)
        return False
    
# 3. 운세 작업 상태 완료 데이터 업데이트 함수
def update_done_date(work, success_count):
    done_serializer = TodaySerializer(work, data={
        'attribute2': 1, 
        'luck_msg' : f'Success count = {success_count}',
        'gpt_id' : 1}, partial=True)
    if done_serializer.is_valid():
        done_serializer.save()
        return True
    else:
        log_error(done_serializer.errors)
        return False

# Error 출력용 함수
def log_error(errors):
    # 오류를 터미널에 출력. 다른 방법도 추가 가능.
    print(errors)

# GPT API 사용 - 오늘의 한마디, 오늘의 띠별 운세, 오늘의 별자리별 운세, 오늘의 mbti별 운세 각각의 함수 이용.
# 1) 특정 일자 오늘의 운세 세트 생성
# /api/v1/gpt/luck/
class GptTodayLuck(APIView):
    #스웨거를 위한 시리얼라이저 설정
    serializer_class = GptLuckSerializer

    #스웨거 API구분을 위한 데코레이터
    @extend_schema(tags=['GPT Prompt'],
        examples=[
            OpenApiExample(
                'Example',
                value={'date' : '20240612'
                },
                request_only=True,  # 요청 본문에서만 예시 사용
            )
        ],
        description="각 category별 프롬프트중에서 가장 최근의 프롬프트메세지를 사용하여 GPT에 운세 생성 요청하여 결과를 DB에 저장.<br>원하는 일자 선정하여 해당 일자로 GPT에게 질문 가능. ex) 일자 예시 : 20240612<br>운세 데이터가 없는 일자에만 생성 가능. 운세 데이터가 있다면 개별 수정 필요.<br><br>[2024.06.10 Update]<br>스케줄러에서는 api 사용 안하고 자동 실행 될 수 있도록, 기간 내 운세 원하거나 특정 일자 운세 원할 경우에는 api 사용할 수 있도록 날짜 입력 받아 작동하는 것으로 변경."
    )

    def post(self, request):
        # POST 요청의 body에서 입력한 일자 'date'를 추출
        request_date = request.data.get('date')

        # success_count 변수값 초기화.
        # global success_count
        success_count = 0

        luck_date = request_date

        # 해당 일자 운세 데이터 작동 했는지 확인.
        work_on = LuckMessage.objects.filter(category='work', luck_date=luck_date, attribute2=0).first()
        # attribute2) 0 : '작업중', 1 : '작업완료'

        if not work_on:
            # 해당 일자 운세 작업을 이전에도 했는지 확인.
            worked = LuckMessage.objects.filter(category='work', luck_date=luck_date, attribute2=1).first()
            if not worked:  # 해당 일자 운세 생성 작업한 적이 없는 경우. (작업 확인 데이터 없는 경우)
                # 해당 일자 작업 확인 데이터 추가.
                if not add_work_date(luck_date):
                    return Response(f"{luck_date} 운세 생성 작업을 확인하기 위한 데이터를 생성하는데 오류가 발생했습니다.",status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:   # 해당 일자 운세 생성 작업한 적이 있는 경우. (작업 확인 데이터 있는 경우)
                # 작업 확인 데이터에 '해당 일자 작업이 이루어지고 있다'로 수정.
                if not update_work_date(worked):
                    return Response(f"{luck_date} 운세 생성 작업을 확인하기 위한 데이터를 업데이트하는데 오류가 발생했습니다.",status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            # 각 카테고리별 GPT에게 질문하는 함수 실행.
            # GptToday(luck_date) # Success count = 1
            # GptStar(luck_date) # Success count = 2
            # GptMbti(luck_date) # Success count = 4
            # GptZodiac1(luck_date) # Success count = 8
            # GptZodiac2(luck_date) # Success count = 16
            success_count += run_gpt_functions(luck_date)

            # 작업이 전부 완료된 뒤 작업 확인 데이터 내용 '완료'로 수정.
            work = LuckMessage.objects.filter(category='work', luck_date=luck_date).first()
            if not update_done_date(work, success_count):
                return Response(f"{luck_date} 운세 생성 작업 확인 데이터를 완료로 업데이트하는데 오류가 발생했습니다.",status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            # 전부 다 작동시 success count 합 31, 이 외 일부만 작동시 해당 success count 확인하여 작동된 함수 유추 가능.
            if success_count == 31:
                return Response(f"{luck_date} 운세 데이터 생성을 완료 했습니다.", status=status.HTTP_200_OK)
            else:
                return Response(f"{luck_date} 운세 데이터가 이미 있습니다.{success_count}", status=status.HTTP_206_PARTIAL_CONTENT)
        else:
            return Response(f"{luck_date} 운세 데이터 생성을 하는 중입니다.", status=status.HTTP_208_ALREADY_REPORTED)


# 2) 원하는 기간 오늘의 운세 세트 생성
# /api/v1/gpt/luck/terms/
class GptLuckPeriod(APIView):
    #스웨거를 위한 시리얼라이저 설정
    serializer_class = GptLuckSerializer

    #스웨거 API구분을 위한 데코레이터
    @extend_schema(tags=['GPT Prompt'],
        examples=[
            OpenApiExample(
                'Example',
                value={'date1' : '20240613',
                        'date2' : '20240713'
                },
                request_only=True,  # 요청 본문에서만 예시 사용
            )
        ],
        description="원하는 기간을 설정 후 각 일자별로 운세를 생성한다. 각 category별 프롬프트중에서 가장 최근의 프롬프트메세지를 사용하여 GPT에 운세 생성 요청하고 결과를 DB에 저장. <br>ex) 일자 예시 : 20240613 / 20240713<br><br>※주의사항<br>- 콘텐츠 자동 생성일 주기(term_date)와 맞물려서 작동되어야 합니다."
    )
    def post(self, request):
        # POST 요청의 body에서 입력한 일자 'date1'과 'date2'를 추출
        request_date1 = request.data.get('date1')   # 20240613
        request_date2 = request.data.get('date2')   # 20240713

        # 문자열을 datetime 객체로 변환하는 함수
        def str_to_date(date_str):
            return datetime.strptime(date_str, '%Y%m%d')
        
        # POST로 요청받은 데이터 날짜 형태로 변환.
        date1 = str_to_date(request_date1)
        date2 = str_to_date(request_date2)

        # 기간 변수 설정
        date_term = (date2 - date1).days

        # 원하는 일자만큼 생성되었는지 확인하기 위한 변수 설정.
        date_count = 0
        
        # 결과 메시지 리스트
        results = []

        for i in range(date_term + 1):  # +1을 해서 마지막 날짜도 포함
            date = date1 + timedelta(days=i)
            luck_date = date.strftime('%Y%m%d')

            # success_count 변수값 초기화.
            # global success_count
            success_count = 0

            # 해당 일자 운세 데이터 작동 했는지 확인.
            work_on = LuckMessage.objects.filter(category='work', luck_date=luck_date, attribute2=0).first()
            # attribute2) 0 : '작업중', 1 : '작업완료'

            if not work_on:
                # 해당 일자 운세 작업을 이전에도 했는지 확인.
                worked = LuckMessage.objects.filter(category='work', luck_date=luck_date, attribute2=1).first()
                if not worked:  # 해당 일자 운세 생성 작업한 적이 없는 경우. (작업 확인 데이터 없는 경우)
                    # 해당 일자 작업 확인 데이터 추가.
                    if not add_work_date(luck_date):
                        return Response(f"{luck_date} 운세 생성 작업을 확인하기 위한 데이터를 생성하는데 오류가 발생했습니다.",status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                else:   # 해당 일자 운세 생성 작업한 적이 있는 경우. (작업 확인 데이터 있는 경우)
                    # 작업 확인 데이터에 '해당 일자 작업이 이루어지고 있다'로 수정.
                    if not update_work_date(worked):
                        return Response(f"{luck_date} 운세 생성 작업을 확인하기 위한 데이터를 업데이트하는데 오류가 발생했습니다.",status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                    
                # 각 카테고리별 GPT에게 질문하는 함수 실행.
                # GptToday(luck_date) # Success count = 1
                # GptStar(luck_date) # Success count = 2
                # GptMbti(luck_date) # Success count = 4
                # GptZodiac1(luck_date) # Success count = 8
                # GptZodiac2(luck_date) # Success count = 16
                success_count += run_gpt_functions(luck_date)

                # 작업이 전부 완료된 뒤 작업 확인 데이터 내용 '완료'로 수정.
                work = LuckMessage.objects.filter(category='work', luck_date=luck_date).first()
                if not update_done_date(work, success_count):
                    return Response(f"{luck_date} 운세 생성 작업 확인 데이터를 완료로 업데이트하는데 오류가 발생했습니다.",status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
                date_count += 1

                # 전부 다 작동시 success count 합 31, 이 외 일부만 작동시 해당 success count 확인하여 작동된 함수 유추 가능.
                if success_count == 31 or success_count == 0:
                    results.append(f"{luck_date} 운세 데이터 생성을 완료했습니다.")
                else:
                    return Response(f"{luck_date} 운세 데이터 생성 중에 오류가 발생했습니다. {results}", status=status.HTTP_417_EXPECTATION_FAILED)
            else:
                return Response(f"{luck_date} 운세 데이터 생성을 하는 중입니다.", status=status.HTTP_208_ALREADY_REPORTED)

        # 원하는 기간만큼 운세가 만들어졌는지 확인.
        if date_count == date_term + 1:
            return Response(f"{request_date1} ~ {request_date2} 기간 동안 {date_count}일 데이터를 완성했습니다.{results}", status=status.HTTP_200_OK)
        else:
            return Response(f"원하는 기간 중 {date_count}일 일부만 만들어졌습니다.{results}", status=status.HTTP_206_PARTIAL_CONTENT)


# 1. 오늘의 한마디 받기 함수
def GptToday(request_date):
    # GPT API Key 설정
    api_key = env.API_KEY
    gpt_client = OpenAI(api_key=api_key)

    # post 요청의 카테고리로 관련 최근 프롬프트메세지 로드
    category = 'today'
    luck_date = request_date
    today_prompt = GptPrompt.objects.filter(category=category).order_by('-gpt_id').first()

    # 오늘의 운세 메세지가 DB에 존재하는지 확인
    find_luck_msg = LuckMessage.objects.filter(category=category, luck_date=luck_date)

    # 프롬프트 메세지 여부 확인
    if not find_luck_msg:
        gpt_id = PromptHistorySerializer(today_prompt).data['gpt_id']
        prefix_prompt = '{"GptResponse":[{"message_num": "1", "luck_msg": "메세지"}]} 예시와 같은 json 형식으로 작성해 줘.'
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
            # model="gpt-4-1106-preview",
            model="gpt-4o",
            messages=messages,
            temperature=0.5,

            # response_format 지정하기
            response_format={"type": "json_object"},
        )

        today_data = json.loads(response.choices[0].message.content)
        
        # today_data 예시
        # today_data = dict(
        #     GptResponse=[
        #         {
        #             'message_num': '1',
        #             'luck_msg': '감성이 풍부해지는 하루가 예상됩니다. 주변 사람들과의 대화에서 위로를 받을 거요. 예술적인 활동에 참여해 보세요.'
        #         }
        #     ]
        # )

        if today_data:

            # [0] 리스트의 요소에 접근하기
            msg = today_data['GptResponse'][0]

            serializer = TodaySerializer(data={
                'luck_date' : luck_date,
                'category' : category,
                'attribute2' : msg['message_num'],
                'luck_msg' : msg['luck_msg'],
                'gpt_id' : gpt_id,
                }
            )
            if serializer.is_valid():
                serializer.save()
            else:
                raise ParseError(serializer.errors)
                
            # prompt의 last_date update
            last_date = luck_date
            today_prompt_last = GptPrompt.objects.filter(category=category).last()

            # 해당 prompt 데이터 찾아서 last_date 데이터 넣기.
            today_prompt_serializer = PromptUpdateSerializer(today_prompt_last, data={'last_date': last_date}, partial=True)

            # 해당 prompt 데이터 찾으면 last_date 업데이트하여 저장.
            if today_prompt_serializer.is_valid():
                today_prompt_serializer.save()

                # # API 요청용 실행 완료 전역 변수
                # global success_count
                # success_count += 1

                return Response(status=status.HTTP_200_OK)
            else:
                return Response(today_prompt_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                # return Response(status=status.HTTP_200_OK)
        else:
            return Response({'detail': '데이터가 없습니다.'},status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'luck_message_today': '이미 데이터가 있습니다.'},status=status.HTTP_206_PARTIAL_CONTENT)
    
# 2. 별자리 운세 받기 함수
def GptStar(request_date):
    # GPT API Key 설정
    api_key = env.API_KEY
    gpt_client = OpenAI(api_key=api_key)

    # post 요청의 카테고리로 관련 최근 프롬프트메세지 로드
    category = 'star'
    luck_date = request_date
    star_prompt = GptPrompt.objects.filter(category=category).order_by('-gpt_id').first()

    # 오늘의 운세 메세지가 DB에 존재하는지 확인
    find_luck_msg = LuckMessage.objects.filter(category=category, luck_date=luck_date)

    # 프롬프트 메세지 여부 확인
    if not find_luck_msg:
        gpt_id = PromptHistorySerializer(star_prompt).data['gpt_id']
        prompt = PromptHistorySerializer(star_prompt).data['prompt_msg']
        prefix_prompt = '{"GptResponse":[{"star": "물병자리", "date_range": "01/20~02/18", "luck_msg": "메세지"}, ...]}예시와 같은 json 형식으로 작성해줘.'
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
            # model="gpt-4-1106-preview",
            model="gpt-4o",
            messages=messages,
            temperature=0.5,

            # response_format 지정하기
            response_format={"type": "json_object"},
        )

        star_data = json.loads(response.choices[0].message.content)

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
                    
                # prompt의 last_date update
                last_date = luck_date
                star_prompt_last = GptPrompt.objects.filter(category=category).last()

                # 해당 prompt 데이터 찾아서 last_date 데이터 넣기.
                star_prompt_serializer = PromptUpdateSerializer(star_prompt_last, data={'last_date': last_date}, partial=True)

                # 해당 prompt 데이터 찾으면 last_date 업데이트하여 저장.
                if star_prompt_serializer.is_valid():
                    star_prompt_serializer.save()

                    # # API 요청용 실행 완료 전역 변수
                    # global success_count
                    # success_count += 2

                    return Response(status=status.HTTP_200_OK)
                else:
                    return Response(star_prompt_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                # return Response(status=status.HTTP_200_OK)
            else:
                return Response({'detail': '데이터가 없습니다.'},status=status.HTTP_400_BAD_REQUEST)

    else:
        return Response({'luck_message_today': '이미 데이터가 있습니다.'},status=status.HTTP_206_PARTIAL_CONTENT)
    
# 3. MBTI 운세 받기 함수
def GptMbti(request_date):
    # GPT API Key 설정
    api_key = env.API_KEY
    gpt_client = OpenAI(api_key=api_key)

    # post 요청의 카테고리로 관련 최근 프롬프트메세지 로드
    category = 'MBTI'

    luck_date = request_date
    mbti_prompt = GptPrompt.objects.filter(category=category).order_by('-gpt_id').first()

    # 오늘의 운세 메세지가 DB에 존재하는지 확인
    find_luck_msg = LuckMessage.objects.filter(category=category, luck_date=luck_date)

    # 프롬프트 메세지 여부 확인
    if not find_luck_msg:
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
            # model="gpt-4o",
            messages=messages,
            temperature=0.5,

            # response_format 지정하기
            response_format={"type": "json_object"},
        )

        mbti_data = json.loads(response.choices[0].message.content)
        # print(mbti_data)

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

                # prompt의 last_date update
                last_date = luck_date
                mbti_prompt_last = GptPrompt.objects.filter(category=category).last()

                # 해당 prompt 데이터 찾아서 last_date 데이터 넣기.
                mbti_prompt_serializer = PromptUpdateSerializer(mbti_prompt_last, data={'last_date': last_date}, partial=True)

                # 해당 prompt 데이터 찾으면 last_date 업데이트하여 저장.
                if mbti_prompt_serializer.is_valid():
                    mbti_prompt_serializer.save()

                    # # API 요청용 실행 완료 전역 변수
                    # global success_count
                    # success_count += 4

                    return Response(status=status.HTTP_200_OK)
                else:
                    return Response(mbti_prompt_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                # return Response(status=status.HTTP_200_OK)
            else:
                return Response({'detail': '데이터가 없습니다.'},status=status.HTTP_400_BAD_REQUEST)
        
    else:
        return Response({'luck_message_today': '이미 데이터가 있습니다.'},status=status.HTTP_206_PARTIAL_CONTENT)
    
# 4. 띠별 운세 받기 함수-1
def GptZodiac1(request_date):
    # GPT API Key 설정
    api_key = env.API_KEY
    gpt_client = OpenAI(api_key=api_key)

    # post 요청의 카테고리로 관련 최근 프롬프트메세지 로드
    category = 'zodiac'
    luck_date = request_date
    zodiac_prompt = GptPrompt.objects.filter(category=category).order_by('-gpt_id').first()

    # 오늘의 운세 메세지가 DB에 존재하는지 확인
    find_luck_msg = LuckMessage.objects.filter(category=category, luck_date=luck_date, attribute1="쥐")

    # 프롬프트 메세지 여부 확인
    if not find_luck_msg:
        gpt_id = PromptHistorySerializer(zodiac_prompt).data['gpt_id']
        prompt_db = PromptHistorySerializer(zodiac_prompt).data['prompt_msg']
        prefix_prompt = '{"GptResponse":[{"zodiac": "닭", "year": "1981", "luck_msg": "메세지"}, ...]}예시와 같은 json 형식으로 작성해줘.'
        prompt_date = luck_date[:4] +'년'+ luck_date[4:6] + '월' + luck_date[6:] + '일 '
        # GPT가 너무 긴 답변을 처리하지 못해서 2파트로 나눠서 요청을 보냄.
        prompt1 = '12간지 중에서 작성해야하는 띠와 태어난 년도야. [쥐]1960년생, 1972년생, 1984년생, 1996년생 (총 4개), [소]1961년생, 1973년생, 1985년생, 1997년생(총 4개), [호랑이]1962년생, 1974년생, 1986년생, 1998년생 (총 4개), [토끼]1963년생, 1975년생, 1987년생, 1999년생 (총 4개), [용]1964년생, 1976년생, 1988년생, 2000년생 (총 4개), [뱀]1965년생, 1977년생, 1989년생, 2001년생 (총 4개) 작성해줘'
        # suffix_prompt2 = '12간지 중에서 작성해야하는 띠와 태어난 년도야. [말]1966년생, 1978년생, 1990년생, 2002년생 (총 4개), [양]1967년생, 1979년생, 1991년생, 2003년생 (총 4개), [원숭이]1968년생, 1980년생, 1992년생, 2004년생 (총 4개), [닭]1969년생, 1981년생, 1993년생, 2005년생 (총 4개), [개]1970년생, 1982년생, 1994년생, 2006년생 (총 4개), [돼지]1971년생, 1983년생, 1995년생, 2007년생 (총 4개) 작성해줘'

        # GPT에게 보낼 질문 메세지
        prompt = prefix_prompt + prompt_date + prompt1 + prompt_db

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
            # model="gpt-4o",
            messages=messages,
            temperature=0.5,

            # response_format 지정하기
            response_format={"type": "json_object"},
        )

        zodiac_data = json.loads(response.choices[0].message.content)
        # print(zodiac_data)
    
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
            # 메세지 처리용 리스트
            zodiac_msg = []
            # DB컬럼에 맞게 dict로 변경
            for msg in zodiac_data['GptResponse']:
                zodiac_msg.append({
                    'attribute1': msg['zodiac'],
                    'attribute2': msg['year'],
                    'luck_msg' :  msg['luck_msg']
                })

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
            
                # prompt의 last_date update
                last_date = luck_date
                zodiac_prompt_last = GptPrompt.objects.filter(category=category).last()

                # 해당 prompt 데이터 찾아서 last_date 데이터 넣기.
                zodiac_prompt_serializer = PromptUpdateSerializer(zodiac_prompt_last, data={'last_date': last_date}, partial=True)

                # 해당 prompt 데이터 찾으면 last_date 업데이트하여 저장.
                if zodiac_prompt_serializer.is_valid():
                    zodiac_prompt_serializer.save()

                    # # API 요청용 실행 완료 전역 변수
                    # global success_count
                    # success_count += 8

                    return Response(status=status.HTTP_200_OK)
                else:
                    return Response(zodiac_prompt_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                # return Response(status=status.HTTP_200_OK)
            else:
                return Response({'detail': '데이터가 없습니다.'},status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'luck_message_today': '이미 데이터가 있습니다.'},status=status.HTTP_206_PARTIAL_CONTENT)

# 5. 띠별 운세 받기 함수-2
def GptZodiac2(request_date):
    # GPT API Key 설정
    api_key = env.API_KEY
    gpt_client = OpenAI(api_key=api_key)

    # post 요청의 카테고리로 관련 최근 프롬프트메세지 로드
    category = 'zodiac'
    luck_date = request_date
    zodiac_prompt = GptPrompt.objects.filter(category=category).order_by('-gpt_id').first()

    # 오늘의 운세 메세지가 DB에 존재하는지 확인
    find_luck_msg = LuckMessage.objects.filter(category=category, luck_date=luck_date, attribute1="말")

    # 프롬프트 메세지 여부 확인
    if not find_luck_msg:
        gpt_id = PromptHistorySerializer(zodiac_prompt).data['gpt_id']
        prompt_db = PromptHistorySerializer(zodiac_prompt).data['prompt_msg']
        prefix_prompt = '{"GptResponse":[{"zodiac": "닭", "year": "1981", "luck_msg": "메세지"}, ...]}예시와 같은 json 형식으로 작성해줘.'
        prompt_date = luck_date[:4] +'년'+ luck_date[4:6] + '월' + luck_date[6:] + '일 '
        # GPT가 너무 긴 답변을 처리하지 못해서 2파트로 나눠서 요청을 보냄.
        # suffix_prompt1 = '12간지 중에서 작성해야하는 띠와 태어난 년도야. [쥐]1960년생, 1972년생, 1984년생, 1996년생 (총 4개), [소]1961년생, 1973년생, 1985년생, 1997년생(총 4개), [호랑이]1962년생, 1974년생, 1986년생, 1998년생 (총 4개), [토끼]1963년생, 1975년생, 1987년생, 1999년생 (총 4개), [용]1964년생, 1976년생, 1988년생, 2000년생 (총 4개), [뱀]1965년생, 1977년생, 1989년생, 2001년생 (총 4개) 작성해줘'
        prompt2 = '12간지 중에서 작성해야하는 띠와 태어난 년도야. [말]1966년생, 1978년생, 1990년생, 2002년생 (총 4개), [양]1967년생, 1979년생, 1991년생, 2003년생 (총 4개), [원숭이]1968년생, 1980년생, 1992년생, 2004년생 (총 4개), [닭]1969년생, 1981년생, 1993년생, 2005년생 (총 4개), [개]1970년생, 1982년생, 1994년생, 2006년생 (총 4개), [돼지]1971년생, 1983년생, 1995년생, 2007년생 (총 4개) 작성해줘'

        # GPT에게 보낼 질문 메세지
        prompt = prefix_prompt + prompt_date + prompt2 + prompt_db

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
            # model="gpt-4o",
            messages=messages,
            temperature=0.5,

            # response_format 지정하기
            response_format={"type": "json_object"},
        )

        zodiac_data = json.loads(response.choices[0].message.content)
        # print(zodiac_data)
    
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
            # 메세지 처리용 리스트
            zodiac_msg = []
            # DB컬럼에 맞게 dict로 변경
            for msg in zodiac_data['GptResponse']:
                zodiac_msg.append({
                    'attribute1': msg['zodiac'],
                    'attribute2': msg['year'],
                    'luck_msg' :  msg['luck_msg']
                })

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
            
                # prompt의 last_date update
                last_date = luck_date
                zodiac_prompt_last = GptPrompt.objects.filter(category=category).last()

                # 해당 prompt 데이터 찾아서 last_date 데이터 넣기.
                zodiac_prompt_serializer = PromptUpdateSerializer(zodiac_prompt_last, data={'last_date': last_date}, partial=True)

                # 해당 prompt 데이터 찾으면 last_date 업데이트하여 저장.
                if zodiac_prompt_serializer.is_valid():
                    zodiac_prompt_serializer.save()

                    # # API 요청용 실행 완료 전역 변수
                    # global success_count
                    # success_count += 16

                    return Response(status=status.HTTP_200_OK)
                else:
                    return Response(zodiac_prompt_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                # return Response(status=status.HTTP_200_OK)
            else:
                return Response({'detail': '데이터가 없습니다.'},status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'luck_message_today': '이미 데이터가 있습니다.'},status=status.HTTP_206_PARTIAL_CONTENT)
