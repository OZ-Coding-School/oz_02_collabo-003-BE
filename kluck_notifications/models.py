from django.db import models

class DeviceToken(models.Model):
    token = models.CharField(max_length=255, unique=True, db_index=True)
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.token
