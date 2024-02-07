from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import VideoflixUser

class AccountAdmin(UserAdmin):
    add_fieldsets = ((None, {"fields": ['username', 'email', 'password1', 'password2']}),)

# Register your models here.
admin.site.register(VideoflixUser, AccountAdmin)