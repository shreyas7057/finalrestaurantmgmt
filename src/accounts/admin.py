from django.contrib import admin

# Register your models here.

from .models import Customer,Staff,Comment


admin.site.register(Customer)
admin.site.register(Staff)
admin.site.register(Comment)