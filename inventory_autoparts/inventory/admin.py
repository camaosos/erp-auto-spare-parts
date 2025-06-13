"""
Admin
"""

from django.contrib import admin
from .models import InventoryItem, Line, ThirdParty, CarBrand, Car, CarYearRange, CarPart

# Register your models here.
admin.site.register(InventoryItem)
admin.site.register(Line)
admin.site.register(ThirdParty)
admin.site.register(CarBrand)
admin.site.register(Car)
admin.site.register(CarYearRange)
admin.site.register(CarPart)
