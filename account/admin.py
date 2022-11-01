from django.contrib import admin
from .models import Profile, User


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_of_birth', 'photo']

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'is_client', 'is_vendor', 'is_staff']
