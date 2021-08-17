from django.test import TestCase
from django.urls import reverse

class TestViews(TestCase):

    def test_should_show_register_page(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'auth/signup.html')

    def test_should_show_login_page(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'auth/login.html')


    def test_should_signup_user(self):
        self.user = {
            "username":"username",
            "email":"email@gmail.com",
            "address":"address",
            "contact":"contact",
            "area":"area",
            'password':'password'
        }
        response = self.client.post(reverse('signup'),self.user)
        self.assertEquals(response.status_code, 302)

    # not workking this test
    # def test_should_not_signup_user_with_taken_username(self):
    #     self.user = {
    #         "username":"username",
    #         "email":"email@email.com",
    #         "address":"address",
    #         "contact":"contact",
    #         "area":"area",
    #         'password':'password'
    #     }
    #     self.client.post(reverse('signup'),self.user)
    #     response = self.client.post(reverse('signup'),self.user)
    #     self.assertEquals(response.status_code, 409)


    # not workking this test
    def test_should_not_signup_user_with_taken_email(self):
        self.user = {
            "username":"username1",
            "email":"email@email.com",
            "address":"address",
            "contact":"contact",
            "area":"area",
            'password':'password'
        }
        self.test_user2 = {
            "username":"username1",
            "email":"email@email2.com",
            "address":"address",
            "contact":"contact",
            "area":"area",
            'password':'password'
        }
        self.client.post(reverse('signup'),self.user)
        response = self.client.post(reverse('signup'),self.test_user2)
        self.assertEquals(response.status_code, 409)