from django.db import models

<<<<<<< HEAD
# Create your models here.
=======

class AdminSetting(models.Model):
    adms_id = models.AutoField(primary_key=True)
    push_time = models.CharField(max_length=4, blank=True, null=True)
    update_date = models.DateTimeField(blank=True, null=True)
>>>>>>> f0f9b72e9f002559ba5a67d98864a3cbe396d455
