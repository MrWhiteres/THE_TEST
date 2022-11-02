"""
Apps auth endpoints.
"""
from django.contrib.auth import views
from django.urls import path, include
from django.views.generic import TemplateView

from .views import Register, BasePageView, UploadCSVView, ProfileView, UploadXMLView

urlpatterns = [
    path('', BasePageView.as_view(), name='base'),
    path('register/', Register.as_view(), name='register'),
    path('auth/', include('django.contrib.auth.urls')),
    path('upload_csv/', UploadCSVView.as_view(), name='upload_csv'),
    path('upload_xml/', UploadXMLView.as_view(), name='upload_xml'),
    path('profile/<int:pk>', ProfileView.as_view(), name='profile')
]
