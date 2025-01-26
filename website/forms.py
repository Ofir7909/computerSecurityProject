from django import forms
from django.conf import settings

MAX_LENGTH = 100


class LoginForm(forms.Form):
    # TODO: change max_length with config file
    username = forms.CharField(label="Username", max_length=MAX_LENGTH)
    password = forms.CharField(
        label="Password",
        max_length=MAX_LENGTH,
        widget=forms.PasswordInput(),
    )


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(label="Enter your email address", required=True)


class ResetPasswordForm(forms.Form):
    token = forms.CharField(
        label="Token",
        required=True,
        max_length=128,
        widget=forms.TextInput(),
    )
    new_password = forms.CharField(
        label="New Password",
        required=True,
        max_length=128,
        widget=forms.PasswordInput(),
    )
    confirm_password = forms.CharField(
        label="Confirm Password",
        required=True,
        max_length=128,
        widget=forms.PasswordInput(),
    )


class RegisterForm(forms.Form):
    # TODO: change max_length with config file
    username = forms.CharField(
        label="Username",
        min_length=3,
        max_length=MAX_LENGTH,
        required=True,
    )
    email = forms.EmailField(label="Email", max_length=MAX_LENGTH, required=True)
    password = forms.CharField(
        label="Password",
        min_length=settings.PASSWORD_REQUIERMENTS.password_length,
        max_length=MAX_LENGTH,
        widget=forms.PasswordInput(),
        required=True,
    )
