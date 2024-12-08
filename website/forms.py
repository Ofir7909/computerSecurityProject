from django import forms


class LoginForm(forms.Form):
    # TODO: change max_length with config file
    username = forms.CharField(label="Username", max_length=100)
    password = forms.CharField(
        label="Password", max_length=100, widget=forms.PasswordInput())
