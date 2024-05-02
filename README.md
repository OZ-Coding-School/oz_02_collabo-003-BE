## 관련 요구사항 ID
- BE-LUCK101 오늘의 한마디
- BE-LUCK202 띠
- BE-LUCK302 별자리
- BE-LUCK402 MBTI

## 모델(models.py)
```py
class LuckMessage(models.Model):
    msg_id = models.AutoField(primary_key=True)
    luck_date = models.CharField(max_length=8, blank=True, null=True)
    category = models.CharField(max_length=50, blank=True, null=True)
    attribute1 = models.CharField(max_length=50, blank=True, null=True)
    attribute2 = models.CharField(max_length=50, blank=True, null=True)
    luck_msg = models.TextField(blank=True, null=True)
    gpt_id = models.IntegerField(null=True)
```

## BE-LUCK101
- 사용자에 맞는 해당 일자의 오늘의 한마디 데이터 로드
- 사용자별 랜덤 오늘의 한마디 고정할 수 있는 방법 고안 필요
- (4/30) 버전 관리를 위해 url 앞에 api/v1 추가.

### 필요 데이터
- 서버상 오늘 날짜
    ```py
    # 오늘 날짜 가져오기, 입력 받은 사용자의 데이터를 변수로 저장.
    now = datetime.now()
    today = now.strftime("%Y%m%d")
    # user_birth = request.GET.get('user_birth')
    # user_MBTI = request.GET.get('user_MBTI')
    ```
    - (4/29) Postman에서 test 해볼 때는 입력되는 user_birth, user_MBTI가 있어서 request로 받았지만
    - (4/30) swagger-ui로 test 해볼 때는 입력되는 값이 필요하여 get에 인자로 추가

### 데이터 호출
- 필터 사용
    ```py
    # 3가지의 오늘의 한마디에서 랜덤하게 제공.
    ran_num = random.randint(0,4)
    today_msg = LuckMessage.objects.filter(luck_date=today, attribute2=ran_num)
    ```

## BE-LUCK202
- 사용자에 맞는 해당 일자의 오늘의 "띠" 운세 데이터 로드

### 필요 데이터
- 사용자 생년월일 데이터(8자리) 중 연도
    ```py
    user_zodiac = user_birth[:4]
    ```

### 데이터 호출
- 필터 사용
    ```py
    zodiac_msg = LuckMessage.objects.filter(luck_date=today, attribute2=user_zodiac)
    ```

## BE-LUCK302
- 사용자에 맞는 해당 일자의 오늘의 "별자리" 운세 데이터 로드

### 필요 데이터
- 사용자 생년월일 데이터(8자리) 중 월, 일 
    ```py
    user_star = int(user_birth[4:])
    ```

### 데이터 호출
- 별자리 구분
    ```py
    if user_star>=120 and user_star<=218:
        star="물병자리"
    elif user_star>=219 and user_star<=320:
        star="물고기자리"
    elif user_star>=321 and user_star<=419:
        star="양자리"
    elif user_star>=420 and user_star<=520:
        star="황소자리"
    elif user_star>=521 and user_star<=620:
        star="쌍둥이자리"
    elif user_star>=621 and user_star<=722:
        star="게자리"
    elif user_star>=723 and user_star<=822:
        star="사자자리"
    elif user_star>=823 and user_star<=922:
        star="처녀자리"
    elif user_star>=923 and user_star<=1022:
        star="천칭자리"
    elif user_star>=1023 and user_star<=1121:
        star="전갈자리"
    elif user_star>=1122 and user_star<=1221:
        star="궁수자리"
    else:
        star="염소자리"
    ```
- 필터 사용
    ```py
    star_msg = LuckMessage.objects.filter(luck_date=today, attribute1=star)
    ```

## BE-LUCK402
- 사용자에 맞는 해당 일자 오늘의 "MBTI" 운세 데이터 로드

### 필요 데이터
- 사용자 mbti 입력 값

### 데이터 호출
- 필터 사용
    ```py
    mbti_msg = LuckMessage.objects.filter(luck_date=today, attribute1=user_MBTI)
    ```

## Serializer - JSON 반환 위함
- serializers.py
    ```py
    from rest_framework import serializers
    from .models import LuckMessage

    class TodayLuckSerializer(serializers.ModelSerializer):
        class Meta:
            model = LuckMessage
            fields = ('luck_date', 'category', 'attribute1', 'attribute2', 'luck_msg')
    ```

- 반영 (views.py)
```py
serializer_class = TodayLuckSerializer
def get(self, request, user_birth, user_MBTI):
    try:
        ...
        today_serializer = TodayLuckSerializer(today_msg[0]).data
        zodiac_serializer = TodayLuckSerializer(zodiac_msg[0]).data
        star_serializer = TodayLuckSerializer(star_msg[0]).data
        mbti_serializer = TodayLuckSerializer(mbti_msg[0]).data

        serializer= {
            'today_msg' : today_serializer,
            'zodiac_msg' : zodiac_serializer,
            'star_msg' : star_serializer,
            'mbti_msg' : mbti_serializer
        }
        
        return Response(serializer, status=status.HTTP_200_OK)

    except LuckMessage.DoesNotExist:
        raise Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
```

## JSON 반환 결과
- 입력값 : {"user_birth" : "19810428", "user_MBTI" : "ESTP"}
```json
{
    "today_msg": {
    "luck_date": "20240429",
    "category": "today",
    "attribute1": null,
    "attribute2": "1",
    "luck_msg": "20240429 오늘의 한마디1번"
    },
    "zodiac_msg": {
        "luck_date": "20240429",
        "category": "zodiac",
        "attribute1": "닭",
        "attribute2": "1981",
        "luck_msg": "20240429 1981 운수"
    },
    "star_msg": {
        "luck_date": "20240429",
        "category": "star",
        "attribute1": "황소자리",
        "attribute2": null,
        "luck_msg": "20240429 taurus 운수"
    },
    "mbti_msg": {
        "luck_date": "20240429",
        "category": "MBTI",
        "attribute1": "ESTP",
        "attribute2": null,
        "luck_msg": "20240429 ESTP 운수"
    }
}
```