"""User form"""
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit

from django import forms
# from django.forms.models import inlineformset_factory
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse
# from crispy_forms.helper import FormHelper, Layout
from .models import BuyItem, InventoryItem, Line, Buy, Sell, SellItem, ThirdParty


class BuyItemForm(forms.ModelForm):
    """ Buy Item Form """
    class Meta:
        model = BuyItem
        fields = ['name', 'item', 'quantity', 'price', 'vat', 'discount']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = True
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-inline'
        self.helper.form_tag = False

        self.helper.layout = Layout(
            Row(
                Column('name', css_class='col-md-4'),
                Column('item', css_class='col-md-4'),
                Column('quantity', css_class='col-md-4'),
                Column('price', css_class='col-md-4'),
                Column('vat', css_class='col-md-4'),
                Column('discount', css_class='col-md-4'),

                css_class='form-row'
            )
        )

        if self.instance and self.instance.pk:
            self.fields['item'].disabled = True  # <-- Esto deshabilita el campo al editar

class SellItemForm(forms.ModelForm):
    """ Buy Item Form """
    class Meta:
        model = SellItem
        fields = ['name', 'item', 'quantity', 'price']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = True
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-inline'
        self.helper.form_tag = False
        
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='col-md-4'),
                Column('item', css_class='col-md-4'),
                Column('quantity', css_class='col-md-4'),
                Column('price', css_class='col-md-4'),
                css_class='form-row'
            )
        )

        if self.instance and self.instance.pk:
            self.fields['item'].disabled = True  # <-- Esto deshabilita el campo al editar


class UserRegisterForm(UserCreationForm):
    """User register form"""
    email = forms.EmailField()
    class Meta:
        """User meta"""
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class InventoryItemForm(forms.ModelForm):
    line = forms.ModelChoiceField(queryset=Line.objects.all())
    # car_year_ranges = forms.ModelMultipleChoiceField(
    #     queryset=InventoryItem.objects.none(),  # Adjust this queryset as needed
    #     required=False,
    #     widget=forms.CheckboxSelectMultiple
    # )
    class Meta:
        model = InventoryItem
        fields = ['name', 'quantity', 'line', 'car_year_ranges']


class LineForm(forms.ModelForm):
    class Meta:
        model = Line
        fields = ['name']


class BuyForm(forms.ModelForm):
    """ Buy Form """
    # name = forms.CharField(required=True)
    # item = forms.ModelChoiceField(queryset=InventoryItem.objects.all(), required=True)
    # quantity = forms.IntegerField(required=True)
    # third_party = forms.ModelChoiceField(queryset=ThirdParty.objects.all(), required=True)
    class Meta:
        model = Buy
        fields = ['name', 'third_party']
    


class SellForm(forms.ModelForm):
    """ Sell Form """
    # name = forms.CharField(required=True)
    # item = forms.ModelChoiceField(queryset=InventoryItem.objects.all(), required=True)
    # third_party = forms.ModelChoiceField(queryset=ThirdParty.objects.all(), required=True)
    class Meta:
        model = Sell
        fields = ['name', 'vat', 'third_party']


class ThirdPartyForm(forms.ModelForm):
    """ Third Party Form """
    name = forms.CharField(required=True)
    surname = forms.CharField(required=True)
    id = forms.CharField(required=True)
    is_provider = forms.BooleanField(required=False)
    is_customer = forms.BooleanField(required=False)
    class Meta:
        model = ThirdParty
        fields = ['name', 'surname', 'id', 'is_provider', 'is_customer']