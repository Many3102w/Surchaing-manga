from django import forms
from django.contrib.auth.models import User
from .models import UserProfile

class UserUpdateForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de usuario'}))

    class Meta:
        model = User
        fields = ['username']

class ProfileUpdateForm(forms.ModelForm):
    avatar = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control'}), required=False)
    role = forms.ChoiceField(choices=UserProfile.ROLE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}), required=False, label="Rol / Título")
    country = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'País'}), required=False)

    class Meta:
        model = UserProfile
        fields = ['avatar', 'role', 'country']
