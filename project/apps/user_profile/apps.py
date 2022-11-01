"""
Register app name for Django
"""

from django.apps import AppConfig


class AuthConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'project.apps.user_profile'
    verbose_name = "Profile"
