from django import forms
from .models import FoodItem

class AddFoodItemForm(forms.ModelForm):
    class Meta:
        model = FoodItem
        fields = ['name', 'price']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}), 
            'price': forms.NumberInput(attrs={'class': 'form-control'}), 
        }

