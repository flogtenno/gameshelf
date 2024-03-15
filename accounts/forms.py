from django import forms

from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'userimage', 'nickname']


class CustomUserEditForm(forms.ModelForm):
    password = forms.CharField(label='パスワード変更', widget=forms.PasswordInput, required=False)
    confirm_password = forms.CharField(label='※変更後パスワード確認:再度入力', widget=forms.PasswordInput, required=False)
    class Meta:
        model = CustomUser
        fields = ['username', 'nickname', 'userimage']

class LoginForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password']