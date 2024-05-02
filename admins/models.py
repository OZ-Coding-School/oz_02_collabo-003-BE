from django.db import models

class Admin(models.Model):
    admins_id = models.AutoField(primary_key=True)
    admin_id = models.CharField(max_length=30, blank=True, null=True)
    admin_user = models.CharField(max_length=30, blank=True, null=True)
    cell_num = models.CharField(max_length=11, blank=True, null=True)
    email = models.CharField(max_length=50, blank=True, null=True)
    create_date = models.DateTimeField(auto_now_add=True)
    permission = models.CharField(max_length=30, blank=True, null=True)
    last_date = models.DateTimeField(null=True)
    user_pw = models.CharField(max_length=100, blank=True, null=True)
    adms_id = models.IntegerField(null=True)