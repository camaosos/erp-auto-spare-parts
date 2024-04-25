"""Models"""
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

# Create your models here.


class InventoryItem(models.Model):
    """Inventory Item"""

    name = models.CharField(_("name"), max_length=200)
    quantity = models.IntegerField(_("quantity"))
    line = models.ForeignKey(to="Line", on_delete=models.SET_NULL, blank=True, null=True, verbose_name=_("line"))
    date_created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Line(models.Model):
    """Line"""

    name = models.CharField(_("name"), max_length=200)
    
    class Meta:
        verbose_name = _("line")

    def __str__(self):
        return self.name
