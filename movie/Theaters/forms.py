from django import forms
from .models import Theater, Screen

class TheaterForm(forms.ModelForm):
    class Meta:
        model = Theater
        fields = ['name',  'location']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}), 
            'location': forms.TextInput(attrs={'class': 'form-control'}), 
        }

class AddScreenForm(forms.ModelForm):
    total_seats = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Screen
        fields = ['name',  'total_seats']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}), 
        }
