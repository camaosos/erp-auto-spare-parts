from django.contrib import admin
from .models import InventoryItem, Line

# Register your models here.
admin.site.register(InventoryItem)
admin.site.register(Line)
