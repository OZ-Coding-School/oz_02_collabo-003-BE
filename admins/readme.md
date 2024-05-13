# 1. 관리자: 로그인 및 리스트 조회

## 1) 관리자 로그인
- 관리자 로그인(관리자 로그인 (최근 접속일 업데이트)

### (0) 모델(models.py)
```py
from django.db import models

class Admin(models.Model):
    admins_id = models.AutoField(primary_key=True)
    admin_id = models.CharField(max_length=30, blank=True, unique=True)
    admin_user = models.CharField(max_length=30, blank=True, null=True)
    cell_num = models.CharField(max_length=11, blank=True, unique=True)
    email = models.CharField(max_length=50, blank=True, unique=True)
    create_date = models.DateTimeField(auto_now_add=True)
    permission = models.CharField(max_length=30, blank=True, null=True)
    last_date = models.DateTimeField(null=True)
    admin_pw = models.CharField(max_length=100, blank=True, null=True)
    adms_id = models.IntegerField(null=True)
```
- (5/3) user_pw -> admin_pw 로 변경

### (1) 관련 요구사항 ID
- BE-ADM001

### (2) 필요 데이터 및 데이터 호출
- admin_id (get)
- admin_pw (get)
- last_date (post)
```py
# api/v1/admin/login/
class AdminLogin(APIView):
    '''
    프론트에서 admin_id(ID), admin_pw(패스워드)를 받아 로그인,
    관리자 로그인 후 최종 접속 날짜(last_date)를 오늘 날짜로 업데이트
    '''
    serializer_class = AdminLoginSerializer
    def post(self, request):
        admin_id = request.data.get('admin_id')
        admin_pw = request.data.get('admin_pw')

        try:
            admin = Admin.objects.get(admin_id=admin_id)
            if check_password(admin_pw, admin.admin_pw):
                # 비밀번호 확인 후 로그인 처리
                admin.last_date = timezone.now()
                admin.save()
                return Response({'message': '로그인 성공'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': '비밀번호가 일치하지 않습니다.'}, status=status.HTTP_401_UNAUTHORIZED)
        except Admin.DoesNotExist:
            return Response({'message': '존재하지 않는 관리자 ID입니다.'}, status=status.HTTP_404_NOT_FOUND)
```

### (3) Serializer - JSON 반환 위함
```py
#/api/v1/admin/login
class AdminLoginSerializer(ModelSerializer):
    '''
    프론트에서 admin_id(ID), user_pw(패스워드)를 받아 로그인,
    관리자 로그인 후 최종 접속 날짜(last_date)를 오늘 날짜로 업데이트
    '''
    class Meta:
        model = Admin
        fields = ('admin_id', 'admin_pw')
```

### (4) URL
```py
path('login/', AdminLogin.as_view(), name='AdminLogin'),
```

## 2) 관리자 리스트 조회
- 관리자 리스트 로드

### (1) 관련 요구사항 ID
- BE-ADM003

### (2) 필요 데이터 및 데이터 호출
- 모든 관리자 데이터 로드
```py
# api/vi/admin/
class AdminUsers(APIView):
    '''
    프론트에서 admins_id(PK), email, admin_user(사용자명), cell_num(폰 번호), create_date(등록일)를 로드
    '''
    serializer_class = AdminSerializer
    def get(self, request):
        admins = Admin.objects.all()
        serializer = AdminSerializer(admins, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
```

### (3) Serializer - JSON 반환 위함
```py
#/api/v1/admin/
class AdminSerializer(ModelSerializer):
    class Meta:
        model = Admin
        fields = ('admins_id', 'admin_user', 'cell_num', 'email', 'create_date', 'last_date')
```

### (4) URL
```py
path('', AdminUsers.as_view(), name='AdminUsers'),
```

## +) 관리자 생성 (For test)
- 관리자 생성 (테스트를 위해 만든 API)

### (1) 관련 요구사항 ID
- BE-ADM002

### (2) 필요 데이터 및 데이터 호출
- admin_id (post)
- admin_pw (post)
```py
# api/v1/admin/signup/
class AdminUsersSignup(APIView):
    '''
    프론트에서 admin_id(ID), admin_user(사용자명), cell_num(폰 번호), email, user_pw(패스워드)를 받아
    관리자 등록 수정 내용을 따로 다시 반환하지는 않는다.
    '''
    serializer_class = AdminSignupSerializer
    def post(self, request):

        password = request.data.get('admin_pw')
        serializer = AdminSignupSerializer(data=request.data)

        try:
            validate_password(password)
        except:
            raise ParseError('Password is invalid.')

        if serializer.is_valid():
            user = serializer.save()
            user.admin_pw = make_password(password)
            user.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            raise ParseError(serializer.errors)
```

### (3) Serializer - JSON 반환 위함
```py
#/api/v1/admin/signup/
class AdminSignupSerializer(ModelSerializer):
    '''
    피그마 화면에서 수정이 가능한 항목만 수정
    '''
    class Meta:
        model = Admin
        fields = ('admin_id', 'admin_user', 'cell_num', 'email', 'admin_pw')
```

### (4) URL
```py
path('signup/', AdminUsersSignup.as_view(), name='AdminUsersSignup'),
```

# 2. 관리자: 메세지관리

## 1) 메세지 종류
 - GPT100 오늘의 한마디 
 - GTP200 띠 메세지 
 - GPT300 별자리 메세지 
 - GPT400 MBTI 메세지 

### (1) 관련 요구사항ID 
 - GPT104 오늘의 한마디 날짜별 로드 
 - GPT105 오늘의 한마디 날짜별 개별 수정 
 - GTP204 띠 메세지 날짜별 로드
 - GTP205 띠 메세지 개별 수정
 - GPT304 별자리 메세지 날짜별 로드
 - GPT305 별자리 메세지 개별 수정
 - GPT404 MBTI 메세지 날짜별 로드 
 - GPT405 MBTI 메세지 개별 수정

### (2) 필요 데이터 및 데이터 호출
- msg_id (get)
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
        fields = ('msg_id', 'luck_msg')
```

### (4) URL
```py
path('msg/', EditLuckMessage.as_view(), name='EditLuckMessage'),
```