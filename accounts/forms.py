from django import forms
from django.contrib.auth.forms import UserCreationForm
from . models import User


class RegisterForm(UserCreationForm):
    phone = forms.CharField(max_length=13, widget=forms.TextInput(attrs={"class": "input-medium bfh-phone", "data-format": "+91dddddddddd"}))

    class Meta:
        model = User
        fields = ('phone', 'email', 'password1', 'password2',)
