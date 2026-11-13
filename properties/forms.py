
from django import forms
from .models import Client, PropertyInquiry


class ClientForm(forms.ModelForm):

    class Meta:
        model = Client
        fields = [
            'name',
            'email',
            'phone',
            'client_type',
            'address',
        ]

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your full name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your email'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter phone number'
            }),
            'client_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
        }


class PropertyInquiryForm(forms.ModelForm):

    class Meta:
        model = PropertyInquiry
        fields = ['message']

        widgets = {
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Write your inquiry here...'
            }),
        }
