from django.db import models

# 사용자 디바이스 토큰 및 앱 이름 저장
class DeviceToken(models.Model):
    token = models.CharField(max_length=255, db_index=True)
    app_name = models.CharField(max_length=100)
    create_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        # 토큰 - 앱의 조합이 고유해야 한다. (같은 토큰 다른 앱)
        unique_together = ('token', 'app_name')  # 복합 인덱스 설정

    def __str__(self):
        return self.token
