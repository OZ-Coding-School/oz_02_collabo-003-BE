from django.db import models
from django.contrib.auth.models import User
from admin_settings.models import AdminSetting

class kluck_Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    cell_num = models.CharField(max_length=11, blank=True, unique=True)

    def __str__(self):
        return self.user.username


    # user table의 id로 대체
    # admins_id = models.AutoField(primary_key=True)
    # user table의 username으로 대체
    # admin_id = models.CharField(max_length=30, blank=True, unique=True)
    # 관리자 이름 사용안함
    # admin_user = models.CharField(max_length=30, blank=True, null=True)
    # user table의 email로 대체
    # email = models.CharField(max_length=50, blank=True, unique=True)
    # user table의 date_joined로 대체
    # create_date = models.DateTimeField(auto_now_add=True)
    # user table의 is_staff로 대체
    # permission = models.CharField(max_length=30, blank=True, null=True)
    # user table의 last_login으로 대체
    # last_date = models.DateTimeField(null=True)
    # user table의 password로 대체
    # admin_pw = models.CharField(max_length=100, blank=True, null=True)
