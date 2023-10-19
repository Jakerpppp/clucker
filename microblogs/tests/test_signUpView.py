from django.test import TestCase
from microblogs.forms import SignUpForms
from microblogs.models import User
from django.urls import reverse

"""Tests of the Sign Up View"""
class SignUpViewTestCase(TestCase):

    def test_sign_up_url(self):
        self.assertEquals(reverse("sign_up"), "/sign_up/")
    
    def test_get_sign_up(self):
        url = reverse("sign_up")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,"sign_up.html")
        form = response.context["form"]
        self.assertTrue(isinstance(form, SignUpForms))  


