from django.test import TestCase
from microblogs.forms import SignUpForms
from microblogs.models import User
from django.urls import reverse
from django.contrib.auth.hashers import check_password

from .helpers import LogInTester

"""Tests of the Sign Up View"""
class SignUpViewTestCase(TestCase, LogInTester):


    def setUp(self):
        self.url = reverse("sign_up")
        self.form_input = {
            "first_name" : "John",
            "last_name" : "Doe",
            "username" :"@johndow1",
            "email" : "johndoe@gmail.com",
            "bio" : "John Doe is a talking head",
            "password" : "UhDoe1",
            "passwordConfirmation" : "UhDoe1"
        }


    def test_sign_up_url(self):
        self.assertEquals(reverse("sign_up"), "/sign_up/")
    
    def test_get_sign_up(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,"sign_up.html")
        form = response.context["form"]
        self.assertTrue(isinstance(form, SignUpForms))  
        self.assertFalse(form.is_bound)

    def test_unsuccessful_sign_up(self):
        self.form_input["username"] = "BAD"
        before_count = User.objects.count()
        response = self.client.post(self.url, self.form_input)
        after_count = User.objects.count()
        self.assertEquals(before_count,after_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,"sign_up.html")
        form = response.context["form"]
        self.assertTrue(isinstance(form, SignUpForms))  
        self.assertTrue(form.is_bound)
        self.assertFalse(self.is_logged_in())

    def test_successful_sign_up(self):
        before_count = User.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count = User.objects.count()
        self.assertEquals(before_count+1,after_count)
        response_url = reverse("feed")
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response,"feed.html")
        user = User.objects.get(username="@johndow1")
        self.assertEqual(user.first_name, "John")
        self.assertEqual(user.last_name, "Doe")
        self.assertEqual(user.email, "johndoe@gmail.com")
        self.assertEqual(user.bio, "John Doe is a talking head")
        is_password_correct = check_password("UhDoe1", user.password)
        self.assertTrue(is_password_correct)
        self.assertTrue(self.is_logged_in())


