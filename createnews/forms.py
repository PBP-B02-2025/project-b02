from django import forms
from createnews.models import News

class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'content', 'category', 'thumbnail', 'is_featured']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Judul berita'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Isi berita'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'thumbnail': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'URL gambar (https://...)'}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
