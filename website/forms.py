from django import forms


class LoginForm(forms.Form):
    # TODO: change max_length with config file
    username = forms.CharField(label="Username", max_length=100)
    password = forms.CharField(
        label="Password", max_length=100, widget=forms.PasswordInput())
<<<<<<< HEAD
    
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


=======


class RegisterForm(forms.Form):
    # TODO: change max_length with config file
    username = forms.CharField(
        label="Username", min_length=3, max_length=100, required=True)
    email = forms.EmailField(
        label="Email", max_length=100, required=True)
    password = forms.CharField(
        label="Password", max_length=100, widget=forms.PasswordInput(), required=True)
>>>>>>> 94b7c229f109d721350d9fe6b69a0605f98b6740
