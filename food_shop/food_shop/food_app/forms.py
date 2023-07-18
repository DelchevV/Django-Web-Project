from django import forms

from .models import CustomUser


class RegisterUserModelForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'age']


class ProfileUpdateModelForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['age', 'birth_date', 'bio', 'profile_picture', 'first_name', 'last_name', ]
