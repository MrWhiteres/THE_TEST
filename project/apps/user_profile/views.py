"""
This module contains all views.
"""
import csv

from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import DetailView, ListView, FormView

from .forms import UserCreationForm, AuthenticationForm, UploadCSVDataForm, UploadXMLDataForm
from .models import UserProfile
from .utils import check_save_data_csv, check_save_data_xml


class Register(View):
    """
    Views for new user registration.
    """
    template_name = 'registration/register.html'

    def get(self, request):
        """
        Base method for views registration.
        """
        context = {
            'form': UserCreationForm(),
        }
        return render(request, self.template_name, context)

    def post(self, request):
        """
        Registration method with data validation and subsequent sending of a message to the mail.
        """
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            login_user =authenticate(username=username, password=password)
            login(request, login_user)
            return redirect('base')
        context = {
            'form': form,
        }
        return render(request, self.template_name, context)


class ProfileView(DetailView):
    """
    User profile views.
    """
    model = UserProfile
    context_object_name = 'profile'
    template_name = 'profile.html'


class MyLoginView(LoginView):  # pylint: disable=too-many-ancestors
    """
    Login views.
    """
    form_class = AuthenticationForm


class BasePageView(ListView):
    def get(self, request, *args, **kwargs):
        users = UserProfile.objects.all()
        context = {
            'profiles': users
        }
        return render(request, 'base.html', context)


class UploadCSVView(FormView):
    template_name = 'upload_csv.html'

    def get(self, request, **kwargs):
        context = {
            'form': UploadCSVDataForm(),
        }
        return render(request, self.template_name, context)

    def post(self, request, **kwargs):
        form = UploadCSVDataForm(request.POST, request.FILES)

        if not form.is_valid():
            return render(request, self.template_name, {'form': UploadCSVDataForm})
        check_save_data_csv(csv.DictReader(request.FILES['csv_file'].read().decode('utf-8').splitlines()))

        return redirect('base')


class UploadXMLView(FormView):
    template_name = 'upload_xml.html'

    def get(self, request, **kwargs):
        context = {
            'form': UploadXMLDataForm(),
        }
        return render(request, self.template_name, context)

    def post(self, request, **kwargs):
        form = UploadXMLDataForm(request.POST, request.FILES)

        if not form.is_valid():
            return render(request, self.template_name, {'form': UploadXMLDataForm})

        check_save_data_xml(request.FILES['xml_file'])
        return redirect('base')

