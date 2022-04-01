from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.core.exceptions import ValidationError
from django.views.generic import FormView


class LoginForm(forms.Form):
    email = forms.CharField(label='email')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)

    def clean(self):
        user = authenticate(
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password']
        )
        if not user:
            raise ValidationError('Введенные данные не верны')
        return self.cleaned_data

# class LoginUserForm(AuthenticationForm):
#
#     email = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
#     password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
#
#
#     def clean(self):
#         user = authenticate(
#             email=self.cleaned_data['email'],
#             password=self.cleaned_data['password']
#         )
#         if not user:
#             raise ValidationError('Введенные данные не верны')
#         return self.cleaned_data

