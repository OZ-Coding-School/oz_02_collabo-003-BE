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
    path("admin/", admin.site.urls),  
    # Optional UI:  
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),  
    # YOUR PATTERNS
    path("api/v1/msg/", include('luck_messages.urls')),
    #오늘의 메세지조회 관련
    path('api/v1/admin/', include('luck_messages.urls_admin')),
    #특정일자 메세지조회 관련
    path('api/v1/admin/', include('admins.urls')),
    #특정 메세지 수정 관련
    path('api/v1/prompt/', include('gpt_prompts.urls')),
]
