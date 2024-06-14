"""
URL configuration for Kluck_config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView


urlpatterns = [
    path("admin/321/123/adm/in/", admin.site.urls),
    # Optional UI:  
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # YOUR PATTERNS
    #오늘의 메세지조회 관련
    path("api/v1/msg/", include('luck_messages.urls')),
    #특정일자 메세지조회 관련
    path('api/v1/admin/', include('luck_messages.urls_admin')),
    #특정 관리자 관련 & 메세지 수정 관련
    # 어드민 테이블 수정으로 주석처리
    path('api/v1/admin/', include('admins.urls')),
    # 프롬프트 gpt 질문 관련
    path('api/v1/prompt/', include('gpt_prompts.urls')),
    path('api/v1/gpt/', include('gpt_prompts.urls_gpt')),
    # 어드민 세팅스 관련
    path('api/v1/adms/', include('admin_settings.urls')),
    # 푸시 알림 관련
    path('api/v1/push/', include('kluck_notifications.urls'))
]
