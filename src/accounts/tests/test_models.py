from accounts.models import Customer
from django.test import TestCase

class TestModel(TestCase):

    def test_should_create_user(self):
        user = Customer.objects.create(
            username='username',
            email='email@email.com',
            address='address',
            area='area',
            contact='1213',
            
        )
        user.set_password('password')

        self.assertEqual(str(user),'email@email.com')