from django.contrib import admin
from WebPage.models import CarModel


@admin.register(CarModel)
class CarsAdmin(admin.ModelAdmin):
    list_display = ('name', 'auction', 'lot_number')
