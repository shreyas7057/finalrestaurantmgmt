from django.contrib import admin

# Register your models here.
from .models import Food,Cart,Order,OrderContent

admin.site.register(Food)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(OrderContent)