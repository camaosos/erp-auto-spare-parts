"""Models"""

# from enum import Enum
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

# Create your models here.

class CarBrand(models.Model):
    """
    Car Brand Model
    """
    name = models.CharField(_("name"), max_length=200, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("car brand")
        verbose_name_plural = _("car brands")

class Car(models.Model):
    """
    Car Model
    """
    name = models.CharField(_("name"), max_length=200)
    brand = models.ForeignKey(CarBrand, on_delete=models.CASCADE, verbose_name=_("brand"))
    model = models.CharField(_("model"), max_length=200)
    line = models.CharField(_("line"), max_length=200, blank=True, null=True)


    def __str__(self):
        return f"{self.brand} {self.model} {self.line}"


class CarYearRange(models.Model):
    """
    Car Model Range
    """
    name = models.CharField(_("name"), max_length=200, default="Default Name")
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    start_year = models.IntegerField(_("start year"))
    end_year = models.IntegerField(_("end year"))

    def __str__(self):
        return f"{self.car.brand} {self.car.model} {self.car.line} ({self.start_year}-{self.end_year})"


class CarPart(models.Model):
    """
    Car Part Model
    """
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    part_name = models.CharField(_("part name"), max_length=200)
    part_number = models.CharField(_("part number"), max_length=200, unique=True)
    description = models.TextField(_("description"), blank=True, null=True)
    car_year_ranges = models.ManyToManyField(CarYearRange, blank=True, verbose_name=_("car year ranges"))

    def __str__(self):
        return f"{self.part_name} ({self.part_number}) for {self.car.brand} {self.car.model}"


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
        verbose_name=_("Line"),
    )
    date_created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    car_year_ranges = models.ManyToManyField(CarYearRange, blank=True, verbose_name=_("car year ranges"))

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

    name = models.CharField(max_length=200, null=False, blank=False, default="predefined", verbose_name=_("Name"))
    date_created = models.DateTimeField(auto_now_add=True)
    # item = models.ForeignKey(
    #     to=InventoryItem, on_delete=models.SET_NULL, blank=True, null=True
    # )
    # quantity = models.IntegerField(_("quantity"), blank=False, default=0)

    third_party = models.ForeignKey(
        to=ThirdParty, on_delete=models.SET_NULL, blank=True, null=True, verbose_name=_("Third party")
    )

    base_total = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00, verbose_name=_("Base total"))

    vat_total = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00, verbose_name=_("VAT total"))
    
    discount_total = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00, verbose_name=_("Discount total"))
    
    total = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00, verbose_name=_("Total"))

    def __str__(self):
        return self.name


class Sell(models.Model):
    """Sell"""

    name = models.CharField(max_length=200, null=False, blank=False, default="predefined", verbose_name=_("Name"))
    date_created = models.DateTimeField(auto_now_add=True)
    vat = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00, verbose_name=_("VAT")
    )
    # item = models.ForeignKey(
    #     to=InventoryItem, on_delete=models.SET_NULL, blank=True, null=True
    # )
    # quantity = models.IntegerField(_("quantity"), blank=False, default=0)

    third_party = models.ForeignKey(
        to=ThirdParty, on_delete=models.SET_NULL, blank=True, null=True, verbose_name=_("Third party")
    )

    base_total = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00, verbose_name=_("Base total"))

    vat_total = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00, verbose_name=_("VAT total"))
    
    total = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00, verbose_name=_("Total"))

    def __str__(self):
        return self.name


class BuyItem(models.Model):
    """
    Buy Item
    """
    buy = models.ForeignKey(Buy, on_delete=models.CASCADE)
    item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, verbose_name=_("Quantity"))
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name=_("Price"))
    vat = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name=_("VAT"))
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name=_("Discount"))
    name = models.CharField(max_length=200, null=True, blank=True, verbose_name=_("Name"))

    def __str__(self):
        return f"{self.item.name} - {self.quantity}"

    # @property
    # def subtotal(self):
    #     return self.quantity * self.price


class SellItem(models.Model):
    """
    Sell Item
    """
    sell = models.ForeignKey(Sell, on_delete=models.CASCADE)
    item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, verbose_name=_("Quantity"))
    # vat = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name=_("VAT"))
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name=_("Price"))
    name = models.CharField(max_length=200, null=True, blank=True, verbose_name=_("Name"))

    def __str__(self):
        return f"{self.item.name} - {self.quantity}"
