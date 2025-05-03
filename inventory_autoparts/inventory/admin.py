"""
Admin
"""

from django.contrib import admin
from .models import InventoryItem, Line, ThirdParty


# Register your models here.
admin.site.register(InventoryItem)
admin.site.register(Line)
admin.site.register(ThirdParty)
