"""Models"""

# from enum import Enum
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

# Create your models here.


class Line(models.Model):
    """Line"""

    name = models.CharField(_("name"), max_length=200)

    class Meta:
        verbose_name = _("line")

    def __str__(self):
        return self.name


class InventoryItem(models.Model):
    """Inventory Item"""

    name = models.CharField(_("name"), max_length=200)
    quantity = models.IntegerField(_("quantity"))
    line = models.ForeignKey(
        to=Line,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name=_("line"),
    )
    date_created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name



class ThirdParty(models.Model):
    """Third Party"""

    is_provider = models.BooleanField()
    is_customer = models.BooleanField()
    # id_type = Enum('Natural Person', 'Legal Person')
    name = models.CharField(_("name"), max_length=200)
    surname = models.CharField(_("surname"), max_length=200)
    id = models.CharField(_("id"), max_length=200, unique=True, primary_key=True)
    # address = models.CharField(_("address"), max_length=200)
    # phone = models.CharField(_("phone"), max_length=200)
    # email = models.EmailField(_("email"), max_length=200, unique=True)
    # date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Buy(models.Model):
    """Buy"""

    name = models.CharField(_("name"), max_length=200, null=False, blank=False, default="predefined")
    date_created = models.DateTimeField(auto_now_add=True)
    # item = models.ForeignKey(
    #     to=InventoryItem, on_delete=models.SET_NULL, blank=True, null=True
    # )
    # quantity = models.IntegerField(_("quantity"), blank=False, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    third_party = models.ForeignKey(
        to=ThirdParty, on_delete=models.SET_NULL, blank=True, null=True
    )

    def __str__(self):
        return self.name


class Sell(models.Model):
    """Sell"""

    name = models.CharField(_("name"), max_length=200)
    date_created = models.DateTimeField(auto_now_add=True)
    # item = models.ForeignKey(
    #     to=InventoryItem, on_delete=models.SET_NULL, blank=True, null=True
    # )
    # quantity = models.IntegerField(_("quantity"), blank=False, default=0)

    third_party = models.ForeignKey(
        to=ThirdParty, on_delete=models.SET_NULL, blank=True, null=True
    )

    def __str__(self):
        return self.name


class BuyItem(models.Model):
    """
    Buy Item
    """
    buy = models.ForeignKey(Buy, on_delete=models.CASCADE)
    item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    name = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f"{self.item.name} - {self.quantity}"

    @property
    def subtotal(self):
        return self.quantity * self.price


class SellItem(models.Model):
    """
    Sell Item
    """
    sell = models.ForeignKey(Sell, on_delete=models.CASCADE)
    item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    name = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f"{self.item.name} - {self.quantity}"
