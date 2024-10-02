from django import forms
from .models import *

class StudentAdmissionForm(forms.ModelForm):
    class Meta:
        model = StudentAdmission
        fields = [
            'first_name', 'last_name', 'date_of_birth', 'gender', 'applying_class', 'previous_school',
            'parent_first_name', 'parent_last_name', 'parent_phone', 'parent_email', 'home_address',
            'emergency_contact_name', 'emergency_contact_phone'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }