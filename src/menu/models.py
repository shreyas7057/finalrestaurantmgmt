from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from accounts.models import Customer,Staff


# Create your models here.

class Food(models.Model):
    dessert = 'Desserts'
    starters = 'Starters Dish'
    main_course = 'Main Course'
    icecreams = 'Cold Drinks'
    
    COURSE = (
        (dessert,dessert),
        (starters,starters),
        (main_course,main_course),
        (icecreams,icecreams),
    )

    disabled = 'Disabled'
    enabled = 'Enabled'

    STATUS = (
        (disabled, disabled),
        (enabled, enabled),
    )

    name = models.CharField(max_length=250)
    course = models.CharField(max_length = 50, choices = COURSE)
    status = models.CharField(max_length=50, choices=STATUS)
    content_description = models.TextField()
    base_price = models.FloatField()
    sale_price = models.FloatField(default=base_price)

    image = models.FileField(upload_to='menu/',blank=True, null =True)
    stock_count = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("all_foods_admin")


class Cart(models.Model):
    quantity = models.IntegerField(default=1)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Order(models.Model):
    pending = 'Pending'
    completed = 'Completed'

    STATUS = (
        (pending,pending),
        (completed,completed),
    )

    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    order_timestamp = models.CharField(max_length=100, blank=True)
    delivery_timestamp = models.CharField(max_length=100, blank=True)
    payment_status = models.CharField(max_length = 100, choices = STATUS)
    delivery_status = models.CharField(max_length = 100, choices = STATUS)
    if_cancelled = models.BooleanField(default = False)
    total_amount = models.IntegerField()
    payment_method = models.CharField(max_length = 100,default="Cash on Delivery")
    location = models.CharField(max_length=200, blank=True, null=True)
    delivery_boy = models.ForeignKey(Staff,on_delete=models.CASCADE, null=True, blank=True)

    def confirmOrder(self):
        self.order_timestamp = timezone.localtime().__str__()[:19]
        self.payment_status = self.completed
        self.save()

    def confirmDelivery(self):
        self.delivery_timestamp = timezone.localtime().__str__()[:19]
        self.delivery_status = self.completed
        self.save()
    
    def __str__(self):
        return self.customer.__str__()


class OrderContent(models.Model):
    quantity = models.IntegerField(default=1)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)