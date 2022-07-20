"""CW URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path, include, re_path
from django.conf.urls.static import static
from CW import settings
from Packs.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth/', include('djoser.urls')),
    path('api/v1/getpacks/', GetPacksAPI.as_view()),
    path('api/v1/upload/', UploadPackAPI.as_view()),
    path('api/v1/download/<str:pk>/', DownloadPackAPI.as_view()),
    path('api/v1/delete/<str:pk>/', DeletePackAPI.as_view()),
    path('api/v1/profile/<str:pk>/', ProfileAPI.as_view()),
    path('api/v1/profile/upload/<str:pk>/', UpdateProfilePicAPI.as_view()),
    path('api/v1/cards/<str:pack>/', GetCardsAPI.as_view()),
    path('rofl', Card.as_view()),
    re_path('api/v1/auth/', include('djoser.urls.authtoken')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

