from django.db import models
from django.utils import timezone

# 사용자 디바이스 토큰 및 앱 이름 저장
class DeviceToken(models.Model):
    token = models.CharField(max_length=255, db_index=True)
    device_os = models.CharField(max_length=100) # 앱 os 구분
    create_date = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)  # token이 마지막으로 업데이트 된 시간 / 유효 토큰 구분
    # app_name = models.CharField(max_length=100) # 프로젝트에 다른 어플이 있을 경우 대비

    class Meta:
        # 토큰 - 앱의 조합이 고유해야 한다. (같은 토큰 다른 앱)
        unique_together = ('token', 'device_os')  # 복합 인덱스 설정

    def __str__(self):
        return self.token
