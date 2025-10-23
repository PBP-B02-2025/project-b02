from django.forms import ModelForm
from userMeasurement.models import userMeasurement
from django import forms


class UserMeasurementForm(ModelForm):
    class Meta:
        model = userMeasurement
        fields = ['height', 'weight', 'waist', 'hip', 'chest']
        widgets = {
            'height': forms.NumberInput(attrs={'class': 'w-full border border-gray-300 rounded-md px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-blue-500'}),
            'weight': forms.NumberInput(attrs={'class': 'w-full border border-gray-300 rounded-md px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-blue-500'}),
            'waist': forms.NumberInput(attrs={'class': 'w-full border border-gray-300 rounded-md px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-blue-500'}),
            'hip': forms.NumberInput(attrs={'class': 'w-full border border-gray-300 rounded-md px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-blue-500'}),
            'chest': forms.NumberInput(attrs={'class': 'w-full border border-gray-300 rounded-md px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-blue-500'}),
        }