from django.db import models

# 사용자 디바이스 토큰 저장
class DeviceToken(models.Model):
    token = models.CharField(max_length=255, unique=True, db_index=True)
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.token
