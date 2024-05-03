# 0. GPT API Test
- 미진행

# 1. 관리자 페이지 -  GPT Prompt 관련 페이지

## 1) 최신 프롬프트 메세지 로드
- 오늘의 한마디/띠별 운세/별자리별 운세/MBTI별 운세에 사용되는 프롬프트 메세지 로드 (최신 1개)

### (0) 모델(models.py)
```py
from django.db import models

class GptPrompt(models.Model):
    gpt_id = models.AutoField(primary_key=True)
    category = models.CharField(max_length=30, blank=True, null=True)
    prompt_msg_name = models.CharField(max_length=100, blank=True, null=True)
    prompt_msg = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=30, blank=True, null=True)
    create_date = models.CharField(max_length=8, blank=True, null=True)
    last_date = models.CharField(max_length=8, blank=True, null=True)
    admins_id = models.IntegerField(null=True)
```
- (4/30) status 행은 사용 X

### (1) 관련 요구사항 ID
- BE-GPT101
- BE-GPT201
- BE-GPT301
- BE-GPT401

### (2) 필요 데이터 및 데이터 호출
- category를 today, zodiac, star, MBTI로 각각 설정하여 로드
```py
# 오늘의 한마디
def get(self, request):
    # 업데이트하는 방식 X, 프롬프트 메세지 이름 사용 X
    try:
        category = "today"
        latest_today = GptPrompt.objects.filter(category=category).order_by('-gpt_id').first()
        serializer = PromptTodaySerializer(latest_today)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except GptPrompt.DoesNotExist:
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

# 띠별 운세
def get(self, request):
    # 업데이트하는 방식 X, 프롬프트 메세지 이름 사용 X
    try:
        category = "zodiac"
        latest_zodiac = GptPrompt.objects.filter(category=category).order_by('-gpt_id').first()
        serializer = PromptZodiacSerializer(latest_zodiac)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except GptPrompt.DoesNotExist:
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

# 별자리별 운세
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

# mbti별 운세
def get(self, request):
    # 업데이트하는 방식 X, 프롬프트 메세지 이름 사용 X
    try:
        category = "mbti"
        latest_mbti = GptPrompt.objects.filter(category=category).order_by('-gpt_id').first()
        serializer = PromptMbtiSerializer(latest_mbti)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except GptPrompt.DoesNotExist:
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
```

### (3) Serializer - JSON 반환 위함
```py
lass PromptTodaySerializer(serializers.ModelSerializer):  # 카테고리별로 작성함.
    class Meta:
            model = GptPrompt
            fields = '__all__'
```

### (4) URL
```py
path('today/', PromptToday.as_view(), name='PromptToday'),
path('zodiac/', PromptZodiac.as_view(), name='PromptZodiac'),
path('star/', PromptStar.as_view(), name='PromptStar'),
path('mbti/', PromptMbti.as_view(), name='PromptMbti')
```

## 2) 프롬프트 메세지 새로 저장
- 사용되는 프롬프트 메시지(GPT API에 적용하는 질문)를 저장합니다.

### (1) 관련 요구사항 ID
- BE-GPT102
- BE-GPT202
- BE-GPT302
- BE-GPT402

### (2) 필요 데이터 및 데이터 호출
- admin_id 확인하고 새로운 프롬프트 질문 저장
```py
# 오늘의 한마디
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

# 띠별 운세
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

# 별자리별 운세
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

# mbti별 운세
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
```

### (3) Serializer - JSON 반환 위함
```py
class PromptTodaySerializer(serializers.ModelSerializer): # 카테고리별로 작성함.
    # 임의로 관리자 id가 1인 자료 생성.
    admins_id = serializers.SerializerMethodField()

    def get_admins_id(self, obj) -> int:
        return 1

    def create(self, validated_data):
        prompt_msg = validated_data.pop('prompt_msg')
        instance = GptPrompt.objects.create(prompt_msg=prompt_msg, **validated_data)
        return instance
```

### (4) URL
- 위 메세지 로드와 동일.

## 3) 프롬프트 메세지 히스토리 로드
- 사용되는 프로프트 메시지(GPT API에 적용하는 질문)들을 가져옵니다. 

### (1) 관련 요구사항 ID
- BE-GPT103
- BE-GPT203
- BE-GPT303
- BE-GPT403

### (2) 필요 데이터 및 데이터 호출
- category를 today, zodiac, star, MBTI로 각각 설정하여 로드
```py
class PromptHistory(APIView):
    # api/v1/prompt/<str:category>/history
    serializer_class = PromptHistorySerializer
    def get(self, request, category):
        try:
            prompt_msgs = GptPrompt.objects.filter(category=category)
            serializer = self.get_serializer(prompt_msgs, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except GptPrompt.DoesNotExist:
            return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
```
- 위에 최신으로 하나 불러오는 것도 이것처럼 한개의 명령으로 합칠 수 있지 않을까?

### (3) Serializer - JSON 반환 위함
```py
class PromptHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model= GptPrompt
        fields = ('gpt_id', 'category', 'prompt_msg_name', 'prompt_msg', 'create_date', 'last_date', 'admins_id')
```

### (4) URL
```py
path('<str:category>/history', PromptHistory.as_view(), name='PromptHistory')
```

## 4) 원하는 날짜, 원하는 카테고리의 프롬프트 메세지 조회
- 오늘의 메시지를 날짜 별로 가져옵니다. (하루 3개)
- 오늘의 운세를 띠별/별자리별/MBTI별 각각 날짜 별로 가져옵니다.

### (1) 관련 요구사항 ID
- BE-GPT104
- BE-GPT204
- BE-GPT304
- BE-GPT404

### (2) 필요 데이터 및 데이터 호출
- category를 today, zodiac, star, MBTI로 각각 설정하여 로드
- luck_date를 오늘로 설정하여 로드
```py
#/api/v1/msg/today/<str:luck_date>
class findSomedayTodayMessages(APIView):
    #특정일자의 Today메세지 조회
    serializer_class = todaySerializer
    def get(self, request, luck_date):
        reqCategory = "today"
        messages = LuckMessage.objects.filter(luck_date=luck_date, category=reqCategory)
        serializer = todaySerializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


#/api/v1/msg/zodiac/<str:luck_date>
class findSomedayZodiacMessages(APIView):
    #특정일자의 띠 메세지 조회
    serializer_class = zodiacSerializer
    def get(self, request, luck_date):
        reqCategory = "zodiac"
        messages = LuckMessage.objects.filter(luck_date=luck_date, category=reqCategory)
        serializer = zodiacSerializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


#/api/v1/admin/star/<str:luck_date>
class findSomedayStarMessages(APIView):
    #특정일자의 별자리 메세지 조회
    serializer_class = starSerializer
    def get(self, request, luck_date):
        reqCategory = "star"
        messages = LuckMessage.objects.filter(luck_date=luck_date, category=reqCategory)
        serializer = starSerializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


#/api/v1/admin/mbti/<str:luck_date>
class findSomedayMbtiMessages(APIView):
    #특정일자의 MBTI 메세지 조회
    serializer_class = mbtiSerializer
    def get(self, request, luck_date):
        reqCategory = 'mbti'
        messages = LuckMessage.objects.filter(luck_date=luck_date, category=reqCategory)
        serializer = mbtiSerializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
```

### (3) Serializer - JSON 반환 위함
```py
class todaySerializer(ModelSerializer):
  #특정 일자의 Today메세지 조회
    class Meta:
        model = LuckMessage
        # fields = '__all__'  # 모든 필드 포함
        fields = ('msg_id', 'luck_date', 'category', 'attribute2', 'luck_msg')

        
class mbtiSerializer(ModelSerializer):
  #특정 일자의 MBTI메세지 조회
    class Meta:
        model = LuckMessage
        # fields = '__all__'  # 모든 필드 포함
        fields = ('msg_id', 'luck_date', 'category', 'attribute1', 'luck_msg')

        
class zodiacSerializer(ModelSerializer):
    class Meta:
        model = LuckMessage
        # fields = '__all__'  # 모든 필드 포함
        fields = ('luck_date', 'category', 'attribute1', 'attribute2', 'luck_msg')

        
class starSerializer(ModelSerializer):
  #특정 일자의 별자리 메세지 조회
    class Meta:
        model = LuckMessage
        # fields = '__all__'  # 모든 필드 포함
        fields = ('msg_id', 'luck_date', 'category', 'attribute1', 'luck_msg')
```

### (4) URL
```py
path('today/<str:luck_date>', findSomedayTodayMessages.as_view(), name='findSomedayTodayMessages'),
path('zodiac/<str:luck_date>', findSomedayZodiacMessages.as_view(), name='findSomedayZodiacMessages'),
path('star/<str:luck_date>', findSomedayStarMessages.as_view(), name='findSomedayStarMessages'),
path('mbti/<str:luck_date>', findSomedayMbtiMessages.as_view(), name="findTodayMbtiMessages")
```

## 5) 특정 메세지 개별 수정
- 관리자가 선택한 운세 메세지 수정

### (1) 관련 요구사항 ID
- BE-GPT105
- BE-GPT205
- BE-GPT305
- BE-GPT405

### (2) 필요 데이터 및 데이터 호출
```py
# api/v1/admin/msg/
class EditLuckMessage(APIView):
    '''
    프론트에서 msg_id를 받아 luck_messages의 모델에서 해당 id를 찾아 내용 수정
    수정 내용을 따로 다시 반환하지는 않는다.
    '''  
    serializer_class = LuckMessageSerializer
    def post(self, request):
        msg_id = request.data.get('msg_id')
        try:
            msg_id = LuckMessage.objects.get(msg_id=msg_id)
        except LuckMessage.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = LuckMessageSerializer(msg_id, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

### (3) Serializer - JSON 반환 위함
```py
#/api/v1/admin/msg/
class LuckMessageSerializer(ModelSerializer):
    #메세지 수정
    class Meta:
        model = LuckMessage
        # fields = '__all__'  # 모든 필드 포함
        fields = ('msg_id', 'luck_msg')
```

### (4) URL
```py
path('msg/', EditLuckMessage.as_view(), name='EditLuckMessage')
```

# 2. GPT API로 받은 응답 저장 (For test)
- 미진행