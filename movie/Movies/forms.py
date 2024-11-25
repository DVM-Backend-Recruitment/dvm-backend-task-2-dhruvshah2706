from django import forms
from .models import Show,  Movie,  Screen,  Theater
from django.utils import timezone

class ScheduleShowForm(forms.ModelForm):
    class Meta:
        model = Show
        fields = ['movie',  'screen',  'start_time',  'ticket_price']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local',  'class': 'form-control'}), 
            'ticket_price': forms.NumberInput(attrs={'class': 'form-control'}), 
        }

    def __init__(self,  *args,  **kwargs):
        self.theater = kwargs.pop('theater',  None)  # Pass the theater instance when initializing the form
        super().__init__(*args,  **kwargs)
        if self.theater:
            self.fields['screen'].queryset = Screen.objects.filter(theater=self.theater)  # Filter screens by theater
        self.fields['movie'].queryset = Movie.objects.all()  
