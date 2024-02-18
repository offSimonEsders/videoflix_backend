"""
URL configuration for videoflix_backend project.

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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from rest_framework import routers

from account.views import RegistrationViewSet, LoginViewSet, LogoutViewSet, CheckTokenView, CheckVerifyTokenView, \
    VerifyUserView
from video.views import VideoView, MediaView

router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('users/register/', RegistrationViewSet.as_view()),
    path('users/login/', LoginViewSet.as_view()),
    path('users/logout/', LogoutViewSet.as_view()),
    path('users/checktoken/', CheckTokenView.as_view()),
    path('users/checkverifytoken/', CheckVerifyTokenView.as_view()),
    path('users/verifyuser/', VerifyUserView.as_view()),
    path('video/', VideoView.as_view()),
    path('media/<path:path>', MediaView.as_view()),
    path('django-rq/', include('django_rq.urls')),
    path('admin/', admin.site.urls)
]
