from django import forms
from .models import User
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm, UserCreationForm

class RegistrationForm(forms.ModelForm):
    username = forms.CharField(label= "Enter Username", min_length=4, max_length=30, help_text="required", widget=forms.TextInput(
        attrs ={"class": "form-control mb-3",
                "placeholder": "Username",
                "id": "register-username"}))
    email = forms.EmailField( max_length=100, help_text="required", error_messages={"required": "Sorry, you will need enter your email address"}, widget=forms.EmailInput(
        attrs ={"class": "form-control mb-3",
                "placeholder": "Email",
                "id": "register-email"}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(
        attrs ={"class": "form-control mb-3",
                "placeholder": "Password",
                "id": "register-pwd"}))
    password2 =  forms.CharField(label="Repeat password", widget=forms.PasswordInput(
        attrs ={"class": "form-control ",
                "placeholder": "Repeat password",
                "id": "register-pwd2"}))
    
    class Meta:
        model = User
        fields = ("username", "email", "first_name",)


class UserLoginForm(AuthenticationForm):
    
    username = forms.CharField(widget=forms.TextInput(
        attrs ={"class": "form-control mb-3",
                "placeholder": "Username",
                "id": "login-username"}))
    
    password = forms.CharField(widget=forms.PasswordInput(
        attrs ={"class": "form-control",
                "placeholder": "Password",
                "id": "login-pwd"}))

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('email',"username")

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('email',"username")
    
