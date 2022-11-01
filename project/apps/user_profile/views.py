"""
This module contains all views.
"""
from django.contrib.auth import authenticate, login
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.contrib.auth.views import LoginView
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils.http import urlsafe_base64_decode
from django.views import View
from django.views.generic import DetailView

from apps.authentication.forms import UserCreationForm, User, AuthenticationForm
from apps.authentication.tasks import send_email_for_verify
from apps.sant.mixins import CartMixin


class Register(CartMixin, View):
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
            'cart': self.cart
        }
        return render(request, self.template_name, context)

    def post(self, request):
        """
        Registration method with data validation and subsequent sending of a message to the mail.
        """
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=password)
            send_email_for_verify(request, user)
            return redirect('confirm_email')
        context = {
            'form': form,
            'cart': self.cart
        }
        return render(request, self.template_name, context)


class ProfileView(DetailView):
    """
    User profile views.
    """
    model = User
    context_object_name = 'profile'
    template_name = 'profile.html'


class MyLoginView(LoginView):  # pylint: disable=too-many-ancestors
    """
    Login views.
    """
    form_class = AuthenticationForm


class LoginAjaxView(View):
    """
    Login with ajax forms.
    """

    def post(self, request):
        """
        The user authorization method checks if the user is in the database
         and checks if there are any errors.
        """
        email = request.POST.get('email')
        password = request.POST.get('password')

        if email and password:
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                return JsonResponse(
                    data={
                        'status': 201
                    },
                    status=200
                )
            return JsonResponse(
                data={
                    'status': 400,
                    'error': 'Пароль и логин не валидные'
                },
                status=200
            )
        return JsonResponse(
            data={
                'status': 400,
                'error': 'Введите логин и пароль'
            },
            status=200
        )

