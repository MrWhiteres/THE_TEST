"""
This file contains registration main models for admin panel
"""
from django.contrib import admin

from .models import UserProfile


@admin.register(UserProfile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user']
