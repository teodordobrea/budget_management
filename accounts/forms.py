from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Account


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name','email', 'password1', 'password2']

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['name', 'slug', 'amount', 'curency', 'type']
        labels = {
            "name": "Name",
            "slug": "Slug",
            "amount": "Amount",
            "curency": "Curency",
            "type": "Type"
        }
