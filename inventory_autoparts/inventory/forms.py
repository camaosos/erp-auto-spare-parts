"""User form"""
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import InventoryItem, Line

class UserRegisterForm(UserCreationForm):
    """User register form"""
    email = forms.EmailField()
    class Meta:
        """User meta"""
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class InventoryItemForm(forms.ModelForm):
    line = forms.ModelChoiceField(queryset=Line.objects.all())
    class Meta:
        model = InventoryItem
        fields = ['name', 'quantity', 'line']

class LineForm(forms.ModelForm):
    class Meta:
        model = Line
        fields = ['name']
        