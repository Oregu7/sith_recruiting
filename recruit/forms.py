from django import forms
from .models import Recruit

class RecruitForm(forms.ModelForm):
    class Meta:
        model = Recruit
        fields = ['name', 'planet', 'age', 'email']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'planet': forms.Select(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'})
        }