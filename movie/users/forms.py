# forms.py in your Users app

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from django.contrib.auth.forms import AuthenticationForm



class ProfileForm(forms.ModelForm):
    ROLE_CHOICES = [
        ('theateradmin',  'Theater Admin'), 
    ]

    role = forms.ChoiceField(choices=ROLE_CHOICES,  widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Profile
        fields = ['role']


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username',  'email',  'password1',  'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}), 
            'email': forms.EmailInput(attrs={'class': 'form-control'}), 
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}), 
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}), 
        }

class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username',  'password')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}), 
            'password': forms.PasswordInput(attrs={'class': 'form-control'}), 
        }

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']

