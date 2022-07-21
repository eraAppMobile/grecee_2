from django import forms
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError


class LoginForm(forms.Form):
    email = forms.CharField(label='email')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)


    def clean(self):
        try:
            user = authenticate(
                email=self.cleaned_data['email'],
                password=self.cleaned_data['password']
            )
        except:
            raise ValidationError(('This account already exists'), code='invalid')
        if not user:
            raise ValidationError(('This account already exists'), code='invalid')
        return self.cleaned_data



