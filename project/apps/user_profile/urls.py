"""
Apps auth endpoints.
"""
from django.contrib.auth import views
from django.urls import path, include
from django.views.generic import TemplateView

from apps.authentication.views import Register, ProfileView, EmailVerify, LoginAjaxView

urlpatterns = [
    path('login_ajax/', LoginAjaxView.as_view(), name="login_ajax"),
    path('register/', Register.as_view(), name='register'),
    path('', include('django.contrib.auth.urls')),
]
