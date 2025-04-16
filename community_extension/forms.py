from django import forms
from .models import Activity

class CreateActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = [
            'title',
            'description',
            'start_date',
            'end_date',
            'time',
            'venue',
            'conducted_by',
            'fees_expenses',
            'attachment'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-md'}),
            'description': forms.Textarea(attrs={'class': 'w-full px-4 py-2 border rounded-md'}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'w-full px-4 py-2 border rounded-md'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'w-full px-4 py-2 border rounded-md'}),
            'time': forms.TimeInput(attrs={'type': 'time', 'class': 'w-full px-4 py-2 border rounded-md'}),
            'venue': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-md'}),
            'conducted_by': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-md'}),
            'fees_expenses': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-md'}),
            'attachment': forms.ClearableFileInput(attrs={'class': 'w-full px-4 py-2 border rounded-md'}),
        }



class UpdateActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = [
            'title', 'description', 'start_date', 'end_date', 
            'time', 'venue', 'conducted_by', 'fees_expenses', 'tags', 'attachment'
        ]
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }