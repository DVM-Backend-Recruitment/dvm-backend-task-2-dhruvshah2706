from django import forms
from Food.models import Order,  FoodItem

class TicketBookingForm(forms.Form):
    num_tickets = forms.IntegerField(
        min_value=1, 
        widget=forms.NumberInput(attrs={'class': 'form-control',  'id': 'num_tickets'}), 
        label="Number of Tickets"
    )

class FoodOrderForm(forms.Form):
    food_item = forms.ModelChoiceField(queryset=FoodItem.objects.none(),  label="Select Food Item")
    quantity = forms.IntegerField(min_value=1,  label="Quantity")

    def __init__(self,  *args,  **kwargs):
        theater = kwargs.pop('theater',  None)
        super().__init__(*args,  **kwargs)
        if theater:
            self.fields['food_item'].queryset = FoodItem.objects.filter(theater=theater.id)


