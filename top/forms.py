from django import forms
from .models import Tag

class CreateTagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['tag']