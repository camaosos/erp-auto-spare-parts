"""User form"""
from django import forms
from django.forms.models import inlineformset_factory
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from crispy_forms.helper import FormHelper, Layout
from .models import BuyItem, InventoryItem, Line, Buy, Sell, SellItem, ThirdParty


class BuyItemForm(forms.ModelForm):
    """ Buy Item Form """
    class Meta:
        model = BuyItem
        fields = ['name', 'item', 'quantity', 'price']


class SellItemForm(forms.ModelForm):
    """ Buy Item Form """
    class Meta:
        model = SellItem
        fields = ['name', 'item', 'quantity', 'price']


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


class BuyForm(forms.ModelForm):
    """ Buy Form """
    name = forms.CharField(required=True)
    # item = forms.ModelChoiceField(queryset=InventoryItem.objects.all(), required=True)
    # quantity = forms.IntegerField(required=True)
    third_party = forms.ModelChoiceField(queryset=ThirdParty.objects.all(), required=True)
    class Meta:
        model = Buy
        fields = ['name', 'third_party']


class SellForm(forms.ModelForm):
    """ Sell Form """
    name = forms.CharField(required=True)
    # item = forms.ModelChoiceField(queryset=InventoryItem.objects.all(), required=True)
    third_party = forms.ModelChoiceField(queryset=ThirdParty.objects.all(), required=True)
    class Meta:
        model = Sell
        fields = ['name', 'third_party']


# class BuyFormSetHelper(FormHelper):
#     """ Buy Form Set Helper """
#     def __init__(self, *args, **kwargs):
#         super(BuyFormSetHelper, self).__init__(*args, **kwargs)
#         self.layout = Layout(
#             'name',
#             'item',
#             'quantity'
#         )
#         self.template = 'bootstrap5/table_inline_formset.html'
#         self.form_tag = False


# class SellFormSetHelper(FormHelper):
#     """ Sell Form Set Helper """
#     def __init__(self, *args, **kwargs):
#         super(SellFormSetHelper, self).__init__(*args, **kwargs)
#         self.layout = Layout(
#             'name',
#             'item',
#             'quantity'
#         )
#         self.template = 'bootstrap5/table_inline_formset.html'
#         self.form_tag = False

# BuyItemFormSet = inlineformset_factory(
#     Buy,
#     BuyItem,
#     fields=['item', 'quantity', 'price'],
#     extra=1,
#     can_delete=True
# )
