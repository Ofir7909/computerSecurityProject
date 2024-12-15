from django import forms


class LoginForm(forms.Form):
    # TODO: change max_length with config file
    username = forms.CharField(label="Username", max_length=100)
    password = forms.CharField(
        label="Password", max_length=100, widget=forms.PasswordInput())


class RegisterForm(forms.Form):
    # TODO: change max_length with config file
    username = forms.CharField(
        label="Username", min_length=3, max_length=100, required=True)
    email = forms.EmailField(
        label="Email", max_length=100, required=True)
    password = forms.CharField(
        label="Password", max_length=100, widget=forms.PasswordInput(), required=True)
