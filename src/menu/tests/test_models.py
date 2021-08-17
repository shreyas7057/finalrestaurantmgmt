from accounts.models import Customer
from menu.models import Food
from django.test import TestCase

class TestModel(TestCase):

    def test_should_create_user(self):
        user = Customer.objects.create(
            username='username',
            email='email@email.com',
            address='address',
            area='area',
            contact=1213,
            
        )
        user.set_password('password')

        menu = Food(
            name='same',
            course='Desserts',
            status='Enabled',
            content_description='dgfdhf',
            base_price=1324,
            sale_price=133
        )
        menu.save()

        self.assertEqual(str(menu),'same')