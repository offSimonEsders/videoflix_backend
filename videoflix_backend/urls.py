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
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path

from rest_framework import routers

from account.views import RegistrationViewSet, LoginViewSet, LogoutViewSet, CheckTokenView, CheckVerifyTokenView, \
    VerifyUserView, SendResetPasswordMail, CheckResetCode, ChangePasswordView
from video.views import MovieView, MediaView, SeriesView, MovieSeriesView

router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('users/register/', RegistrationViewSet.as_view(), name='register'),
    path('users/login/', LoginViewSet.as_view(), name='login'),
    path('users/logout/', LogoutViewSet.as_view(), name='logout'),
    path('users/checktoken/', CheckTokenView.as_view(), name='checktoken'),
    path('users/checkverifytoken/', CheckVerifyTokenView.as_view(), name='checkverifytoken'),
    path('users/verifyuser/', VerifyUserView.as_view(), name='verifyuser'),
    path('users/requestresetpassword/', SendResetPasswordMail.as_view(), name='requestresetpassword'),
    path('users/checkresetcode/', CheckResetCode.as_view(), name='checkresetcode'),
    path('users/changepassword/', ChangePasswordView.as_view(), name='changepassword'),
    path('movies/', MovieView.as_view(), name='movies'),
    path('series/', SeriesView.as_view(), name='series'),
    path('moviesandseries/', MovieSeriesView.as_view(), name='moviesandseries'),
    path('media/<path:path>', MediaView.as_view()),
    path('django-rq/', include('django_rq.urls')),
    path('admin/', admin.site.urls)
] + staticfiles_urlpatterns()
