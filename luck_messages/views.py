from django.shortcuts import render
from .models import LuckMessage
from datetime import datetime
from django.http import HttpResponse
from .serializers import messagesSerializer


def findZodiacMessages(request, attribute1):
    now = datetime.now()
    date = now.strftime("%Y%m%d")
    reqCategory = "zodiac"
    messages = LuckMessage.objects.filter(luck_date=date, category=reqCategory, attribute1=attribute1)
    serializer = messagesSerializer(messages, many=True)
    return HttpResponse(serializer.data)

def findStarMessages(request):
    now = datetime.now()
    date = now.strftime("%Y%m%d")
    reqCategory = "star"
    messages = LuckMessage.objects.filter(luck_date=date, category=reqCategory)
    serializer = messagesSerializer(messages, many=True)
    return HttpResponse(serializer.data)

def findMbtiMessages(request):
    now = datetime.now()
    date = now.strftime("%Y%m%d")
    reqCategory = 'mbti'
    messages = LuckMessage.objects.filter(luck_date=date, category=reqCategory)
    serializer = messagesSerializer(messages, many=True)
    print(serializer.data)
    return HttpResponse(serializer.data)
