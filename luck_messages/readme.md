# 관련 요구사항 ID
- BE-LUCK201 띠
- BE-LUCK301 별자리
- BE-LUCK401 MBTI

### 모델(models.py)
```
class LuckMessage(models.Model):
    msg_id = models.AutoField(primary_key=True)
    luck_date = models.CharField(max_length=8, blank=True, null=True)
    category = models.CharField(max_length=50, blank=True, null=True)
    attribute1 = models.CharField(max_length=50, blank=True, null=True)
    attribute2 = models.CharField(max_length=50, blank=True, null=True)
    luck_msg = models.TextField(blank=True, null=True)
    gpt_id = models.IntegerField(null=True)
```
## BE-LUCK201
- 오늘 날짜의 띠별 모든 년도 데이터 로드
- RestAPI 방식으로 변경
### 필요데이터 
- 오늘날짜
  ```
  class findZodiacMessages(views.APIView):
      serializer_class = zodiacSerializer
      def get(self, request, attribute1):
          now = datetime.now()
          date = now.strftime("%Y%m%d")
          reqCategory = "zodiac"
  ```
### 데이터 호출
- 필터 사용
```
    messages = LuckMessage.objects.filter(luck_date=date, category=reqCategory, attribute1=attribute1)
```


## BE-LUCK301, BE-LUCK401
- 오늘 날짜의 MBTI 모든 종류별 데이터 로드

### 필요데이터 
- 오늘날짜
  ```
  class findStarMessages(views.APIView):
      serializer_class = starSerializer
      def get(self, request):
          now = datetime.now()
          date = now.strftime("%Y%m%d")
          reqCategory = "star"
  ```
### 데이터 호출
- 필터 사용
```
    messages = LuckMessage.objects.filter(luck_date=date, category=reqCategory)
```

### JSON으로 반환하기위한 Serializer
```
  from rest_framework.serializers import ModelSerializer
  from .models import LuckMessage

  class messagesSerializer(ModelSerializer):
    class Meta:
        model = LuckMessage
        fields = ('luck_date', 'category', 'attribute1', 'attribute2', 'luck_msg')
```

### JSON으로 반환
```
  serializer = zodiacSerializer(messages, many=True)
  return Response(serializer.data, status=status.HTTP_200_OK)
```

### JSON 반환 결과
```
  [
    {
        "luck_date": "20240430",
        "category": "zodiac",
        "attribute1": "소",
        "attribute2": "2009",
        "luck_msg": "20240430 2009 운수"
    },
    {
        "luck_date": "20240430",
        "category": "zodiac",
        "attribute1": "소",
        "attribute2": "1997",
        "luck_msg": "20240430 1997 운수"
    },
    {
        "luck_date": "20240430",
        "category": "zodiac",
        "attribute1": "소",
        "attribute2": "1985",
        "luck_msg": "20240430 1985 운수"
    },
    {
        "luck_date": "20240430",
        "category": "zodiac",
        "attribute1": "소",
        "attribute2": "1973",
        "luck_msg": "20240430 1973 운수"
    }
]
```
