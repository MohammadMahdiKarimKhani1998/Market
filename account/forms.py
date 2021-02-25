from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import User


class UserForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = User
        fields = ('email',)


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('email',)


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'مثل : Email@gmail.com'}),
        label='Email')
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Password'}),
        label='Password')

    class Meta:
        fields = ['email', 'password']


class UserRegistrationForm(UserCreationForm):
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={'autocomplete': 'new-password', 'class': 'form-control', 'placeholder': 'حداقل - 8 کاراکتر'}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(
            attrs={'autocomplete': 'new-password', 'class': 'form-control', 'placeholder': 'تکرار رمز عبور'}),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )
    image = forms.ImageField(label='Photo', required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'mobile']
        widgets = {'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'مثال : علی'}),
                   'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'مثال : محمدی'}),
                   'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'مثال : Email@gmail.com'}),
                   'mobile': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+98 9** *******'}), }
