"""Models"""
from enum import Enum
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
    line = models.ForeignKey(to=Line, on_delete=models.SET_NULL, blank=True, null=True, verbose_name=_("line"))
    date_created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Buy(models.Model):
    """ Buy """
    name = models.CharField(_("name"), max_length=200, null=False, blank=False)
    date_created = models.DateTimeField(auto_now_add=True)
    item = models.ForeignKey(to=InventoryItem, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(_("quantity"), blank=False, default=0)

    def __str__(self):
        return self.name

class Sell(models.Model):
    """ Sell """
    name = models.CharField(_("name"), max_length=200)
    date_created = models.DateTimeField(auto_now_add=True)
    item = models.ForeignKey(to=InventoryItem, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(_("quantity"), blank = False, default=0)

    def __str__(self):
        return self.name

class ThirdParty(models.Model):
    """ Third Party """
    is_provider = models.BooleanField()
    is_customer = models.BooleanField()
    # id_type = Enum('Natural Person', 'Legal Person')
    name = models.CharField(_("name"), max_length=200)
    surname = models.CharField(_("surname"), max_length=200)