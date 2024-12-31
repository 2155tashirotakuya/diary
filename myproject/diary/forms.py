from django.forms import ModelForm
from django import forms
from .models import Page


class PageForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = ["title", "body", "page_date","picture"]
        # 改造部分
        widgets = {
            'body':forms.Textarea(attrs={'class': 'diary-textarea'}),
            'page_date': forms.DateInput(attrs={'type':'date'}),
        }

