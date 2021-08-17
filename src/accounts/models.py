from django.db import models

# Create your models here.
from django.contrib.auth.models import User


class Customer(models.Model):
    customer = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    address = models.TextField()
    area = models.CharField(max_length=100,default='')
    contact = models.CharField(max_length = 10)
    orders = models.IntegerField(default=0)
    total_sale = models.IntegerField(default=0)

    def __str__(self):
        return self.customer.username


class Staff(models.Model):
    admin = 'Admin'
    deliveryboy = 'Delivery Boy'
    chef = 'Chef'

    ROLES = (
        (admin,admin),
        (chef,chef),
        (deliveryboy,deliveryboy),
    )
    
    staff_id = models.OneToOneField(User, on_delete=models.CASCADE,primary_key=True)
    address = models.TextField()
    contact = models.CharField(max_length = 10)
    salary = models.IntegerField()
    role = models.CharField(max_length = 30, choices = ROLES)
    
    def __str__(self):
        return self.staff_id.username


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=250)