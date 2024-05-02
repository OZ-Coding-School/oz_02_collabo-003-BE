from django.test import TestCase
from .models import LuckMessage

class LuckMessageModelTest(TestCase):

    def setUp(self):
        LuckMessage.objects.create(
            luck_date = '20240429',
            category = 'MBTI',
            attribute1 = 'ESTP',
            luck_msg = 'ESTP야 개발잘하자!',
            gpt_id = 1
        )
        LuckMessage.objects.create(
            luck_date='20240430',
            category='MBTI',
            attribute1='ENTP',
            luck_msg='ENTP야 개발잘하자!',
            gpt_id=1
        )

    def test_find_luck_message(self):
        message = LuckMessage.objects.get(luck_date='20240429')
        self.assertEqual(message.luck_msg, 'ESTP야 개발잘하자!')
        self.assertEqual(message.category, 'MBTI')
        self.assertEqual(message.attribute1, 'ESTP')
        self.assertEqual(message.gpt_id, 1)

    def test_find_filter_luck_message(self):
        messages = LuckMessage.objects.filter(category='MBTI')
        self.assertEqual(len(messages), 2)
        self.assertEqual(messages[1].attribute1, 'ENTP')