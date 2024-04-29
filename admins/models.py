from django.db import models

<<<<<<< HEAD
# Create your models here.
=======
class Admin(models.Model):
    admins_id = models.AutoField(primary_key=True)
    admin_id = models.CharField(max_length=30, blank=True, null=True)
    admin_user = models.CharField(max_length=30, blank=True, null=True)
    cell_num = models.CharField(max_length=11, blank=True, null=True)
    email = models.CharField(max_length=50, blank=True, null=True)
    create_date = models.CharField(max_length=8, blank=True, null=True)
    permission = models.CharField(max_length=30, blank=True, null=True)
    user_pw = models.CharField(max_length=100, blank=True, null=True)
    adms_id = models.IntegerField(null=True)
>>>>>>> f0f9b72e9f002559ba5a67d98864a3cbe396d455
