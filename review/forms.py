from django.forms import ModelForm
from review.models import Review
from django import forms

class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ["comment", "star"]