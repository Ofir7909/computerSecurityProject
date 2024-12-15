from django import forms


class LoginForm(forms.Form):
    # TODO: change max_length with config file
    username = forms.CharField(label="Username", max_length=100)
    password = forms.CharField(
        label="Password", max_length=100, widget=forms.PasswordInput())
    
class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(label="Enter your email address", required=True)

class ResetPasswordForm(forms.Form):
    current_password = forms.CharField(
        label="Current Password", 
        required=True, 
        max_length=128, 
        widget=forms.PasswordInput()
    )
    new_password = forms.CharField(
        label="New Password", 
        required=True, 
        max_length=128, 
        widget=forms.PasswordInput()
    )
    confirm_password = forms.CharField(
        label="Confirm Password", 
        required=True, 
        max_length=128, 
        widget=forms.PasswordInput()
    )


