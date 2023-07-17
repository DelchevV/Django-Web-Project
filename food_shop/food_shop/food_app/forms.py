from django import forms

from .models import CustomUser


class RegisterUserModelForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username','email','password','age']