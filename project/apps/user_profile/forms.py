# """
# Creation of forms for registration, user authorization
# """
# from django import forms
# from django.contrib.auth import get_user_model, authenticate
# from django.contrib.auth.forms import (
#     UserCreationForm as DjangoUserCreationForm,
#     AuthenticationForm as DjangoAuthenticationForm,
# )
# from django.core.exceptions import ValidationError
# from django.utils.translation import gettext_lazy as _
#
#
# User = get_user_model()
#
#
# class UserCreationForm(DjangoUserCreationForm):
#     """
#     New user registration form.
#     """
#     username = forms.CharField(
#         label=_("Username"),
#         max_length=20,
#         widget=forms.TextInput(attrs={'class': 'form-control'})
#     )
#
#     first_name = forms.CharField(
#         label=_("First name"),
#         max_length=20,
#         widget=forms.TextInput(attrs={'class': 'form-control'})
#     )
#
#     last_name = forms.CharField(
#         label=_("Last name"),
#         max_length=20,
#         widget=forms.TextInput(attrs={'class': 'form-control'})
#     )
#
#     password1 = forms.CharField(
#         widget=forms.PasswordInput(attrs={'class': 'form-control'})
#     )
#
#     password2 = forms.CharField(
#         widget=forms.PasswordInput(attrs={'class': 'form-control'})
#     )
#
#     phone_number = PhoneNumberField(
#         label=_("Phone number"),
#         widget=PhoneNumberPrefixWidget(initial='UA',
#                                        attrs={'class': 'form-control', 'placeholder': 'Введите свой номер телефона'})
#     )
#
#     class Meta(DjangoUserCreationForm.Meta):
#         model = User
#         fields = [
#             'username',
#             'first_name',
#             'last_name',
#             'email',
#             'password1',
#             'password2',
#             'phone_number'
#         ]
#
#
# class AuthenticationForm(DjangoAuthenticationForm):
#     """
#     Base user form for auth.
#     """
#
#     def clean(self):
#         """
#         The function takes values from the form and checks
#          its validity and the existence of a user with such data.
#         """
#
#         username = self.cleaned_data.get('username')
#         password = self.cleaned_data.get('password')
#
#         if username is not None and password:
#             self.user_cache = authenticate(
#                 self.request,
#                 username=username,
#                 password=password,
#             )
#             if not self.user_cache.email_verify:
#                 send_email_for_verify(self.request, self.user_cache)
#                 raise ValidationError(
#                     'Email not verify, check your email',
#                     code='invalid_login',
#                 )
#
#             if self.user_cache is None:
#                 raise self.get_invalid_login_error()
#             else:
#                 self.confirm_login_allowed(self.user_cache)
#
#         return self.cleaned_data
#
#
# class AuthenticationAjaxForm(forms.Form):
#     """
#     Ajax user form for auth.
#     """
#
#     email = forms.EmailField(
#         label=_("Email"),
#         max_length=254,
#         widget=forms.EmailInput(
#             attrs={
#                 'autocomplete': 'email',
#                 'class': 'form-control'
#             }
#         )
#     )
#     password = forms.CharField(
#         label=_("Password"),
#         strip=False,
#         widget=forms.PasswordInput(
#             attrs={
#                 "autocomplete": "current-password",
#                 'class': 'form-control'
#             }
#         ),
#     )
