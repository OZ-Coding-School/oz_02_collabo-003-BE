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

### 필요데이터 
- 오늘날짜
  ```
  def findZodiacMessages(request, attribute1):
    now = datetime.now()
    date = now.strftime("%Y%m%d")
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
    now = datetime.now()
    date = now.strftime("%Y%m%d")
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
    serializer = messagesSerializer(messages, many=True)
    return HttpResponse(serializer.data)
```

### JSON 반환 결과
```
  [{'msg_id': 427, 'luck_date': '20240429', 'category': 'MBTI', 'attribute1': 'ISTJ', 'attribute2': None, 'luck_msg': '20240429 ISTJ 운수', 'gpt_id': 1}, {'msg_id': 428, 
'luck_date': '20240429', 'category': 'MBTI', 'attribute1': 'ISFJ', 'attribute2': None, 'luck_msg': '20240429 ISFJ 운수', 'gpt_id': 1}, {'msg_id': 429, 'luck_date': '202
40429', 'category': 'MBTI', 'attribute1': 'INFJ', 'attribute2': None, 'luck_msg': '20240429 INFJ 운수', 'gpt_id': 1}, {'msg_id': 430, 'luck_date': '20240429', 'category
': 'MBTI', 'attribute1': 'INTJ', 'attribute2': None, 'luck_msg': '20240429 INTJ 운수', 'gpt_id': 1}, {'msg_id': 431, 'luck_date': '20240429', 'category': 'MBTI', 'attri
bute1': 'ISTP', 'attribute2': None, 'luck_msg': '20240429 ISTP 운수', 'gpt_id': 1}, {'msg_id': 432, 'luck_date': '20240429', 'category': 'MBTI', 'attribute1': 'ISFP', '
attribute2': None, 'luck_msg': '20240429 ISFP 운수', 'gpt_id': 1}, {'msg_id': 433, 'luck_date': '20240429', 'category': 'MBTI', 'attribute1': 'INFP', 'attribute2': None
, 'luck_msg': '20240429 INFP 운수', 'gpt_id': 1}, {'msg_id': 434, 'luck_date': '20240429', 'category': 'MBTI', 'attribute1': 'INTP', 'attribute2': None, 'luck_msg': '20
240429 INTP 운수', 'gpt_id': 1}, {'msg_id': 435, 'luck_date': '20240429', 'category': 'MBTI', 'attribute1': 'ESTP', 'attribute2': None, 'luck_msg': '20240429 ESTP 운수'
, 'gpt_id': 1}, {'msg_id': 436, 'luck_date': '20240429', 'category': 'MBTI', 'attribute1': 'ESFP', 'attribute2': None, 'luck_msg': '20240429 ESFP 운수', 'gpt_id': 1}, {
'msg_id': 437, 'luck_date': '20240429', 'category': 'MBTI', 'attribute1': 'ENFP', 'attribute2': None, 'luck_msg': '20240429 ENFP 운수', 'gpt_id': 1}, {'msg_id': 438, 'l
uck_date': '20240429', 'category': 'MBTI', 'attribute1': 'ENTP', 'attribute2': None, 'luck_msg': '20240429 ENTP 운수', 'gpt_id': 1}, {'msg_id': 439, 'luck_date': '20240
429', 'category': 'MBTI', 'attribute1': 'ESTJ', 'attribute2': None, 'luck_msg': '20240429 ESTJ 운수', 'gpt_id': 1}, {'msg_id': 440, 'luck_date': '20240429', 'category':
 'MBTI', 'attribute1': 'ESFJ', 'attribute2': None, 'luck_msg': '20240429 ESFJ 운수', 'gpt_id': 1}, {'msg_id': 441, 'luck_date': '20240429', 'category': 'MBTI', 'attribu
te1': 'ENFJ', 'attribute2': None, 'luck_msg': '20240429 ENFJ 운수', 'gpt_id': 1}, {'msg_id': 442, 'luck_date': '20240429', 'category': 'MBTI', 'attribute1': 'ENTJ', 'attribute2': None, 'luck_msg': '20240429 ENTJ 운수', 'gpt_id': 1}]
```
