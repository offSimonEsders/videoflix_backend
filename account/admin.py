from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import VideoflixUser

class AccountAdmin(UserAdmin):
    add_fieldsets = ((None, {"fields": ['username', 'email', 'password1', 'password2']}),)
    fieldsets = [
        ('Title', {
            'fields': [
                'username',
                'email',
                'verified',
                'verification_code',
                'reset_code',
                'password'
            ],
        }),
    ]
    list_display = ('username', 'email', 'verified')

# Register your models here.
admin.site.register(VideoflixUser, AccountAdmin)