from gpt_prompts.models import *

class LuckMessage(models.Model):
    msg_id = models.AutoField(primary_key=True)
    luck_date = models.CharField(max_length=8, blank=True, null=True)
    category = models.CharField(max_length=50, blank=True, null=True)
    attribute1 = models.CharField(max_length=50, blank=True, null=True)
    attribute2 = models.CharField(max_length=50, blank=True, null=True)
    luck_msg = models.TextField(blank=True, null=True)
    gpt_id = models.ForeignKey(GptPrompt, on_delete=models.PROTECT, db_column='gpt_id')
