from django.db import models


class AdminSetting(models.Model):
    adms_id = models.AutoField(primary_key=True)
    push_time = models.CharField(max_length=4, default='0800')
    term_date = models.CharField(max_length=4, default='0030')
    term_time = models.CharField(max_length=4, default='0110')
    update_date = models.DateTimeField(auto_now=True)

