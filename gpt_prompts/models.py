from admins.models import *

class GptPrompt(models.Model):
    gpt_id = models.AutoField(primary_key=True)
    category = models.CharField(max_length=30, blank=True, null=True)
    prompt_msg = models.TextField(blank=True, null=True)
    create_date = models.CharField(max_length=8, blank=True, null=True)
    last_date = models.CharField(max_length=8, blank=True, null=True)
    user_id = models.ForeignKey(kluck_Admin, on_delete=models.PROTECT, db_column='user_id')
