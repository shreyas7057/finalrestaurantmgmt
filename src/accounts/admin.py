from django.contrib import admin

# Register your models here.

from .models import Customer,Staff


admin.site.register(Customer)
admin.site.register(Staff)