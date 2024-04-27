from django.db import models


class AdminSetting(models.Model):
    adms_id = models.AutoField(primary_key=True)
    push_time = models.CharField(max_length=4, blank=True, null=True)
    update_date = models.DateTimeField(blank=True, null=True)