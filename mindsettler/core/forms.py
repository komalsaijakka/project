from django import forms
from .models import Appointment

class BookingForm(forms.ModelForm):
    # Customizing the datetime input if needed, but for now relying on model defaults or simple widgets
    class Meta:
        model = Appointment
        fields = ['session_type', 'start_time']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        }

    def clean_start_time(self):
        start_time = self.cleaned_data['start_time']
        # Add any specific validation (e.g., business hours) here
        return start_time
