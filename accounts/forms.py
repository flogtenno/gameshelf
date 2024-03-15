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

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get("password")
        if password:
            user.set_password(password)
            if commit:
                user.save()
        return user

class LoginForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password']