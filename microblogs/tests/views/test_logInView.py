from django.test import TestCase
from microblogs.forms import LogInForm
from django.urls import reverse

from microblogs.models import User
from ..helpers import LogInTester

from django.contrib import messages

from ..helpers import reverse_with_next

"""Tests of the Log In View"""
class LogInViewTestCase(TestCase, LogInTester):

    fixtures = ["microblogs/tests/fixtures/default_user.json"]


    def setUp(self):
        self.url = reverse("log_in")
        self.user = User.objects.get(username = "@janedoe")
        self.form_input = {
            "username" :"@janedoe",
            "password" : "Password123",
        }


    def test_log_in_url(self):
        self.assertEquals(reverse("log_in"), "/log_in/")
    
    def test_get_log_in(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,"log_in.html")
        form = response.context["form"]
        next = response.context["next"]
        self.assertTrue(isinstance(form, LogInForm))  
        self.assertFalse(next)
        self.assertFalse(form.is_bound)

    def test_get_log_in_with_redirect(self):
        destination_url = reverse("user_list")
        self.url = reverse_with_next("log_in", destination_url)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,"log_in.html")
        form = response.context["form"]
        next = response.context["next"]
        self.assertTrue(isinstance(form, LogInForm))  
        self.assertEqual(next, destination_url)
        self.assertFalse(form.is_bound)

    def test_unsuccessful_log_in(self):
        form_input = {"username": "noDoe", "password": "NotCorrect"}
        response = self.client.post(self.url, form_input)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,"log_in.html")
        form = response.context["form"]
        self.assertTrue(isinstance(form, LogInForm))  
        self.assertTrue(form.is_bound)
        self.assertFalse(self.is_logged_in())
        messages_list = list(response.context["messages"])
        self.assertEquals(len(messages_list), 1)
        self.assertEquals(messages_list[0].level, messages.ERROR)

    def test_successful_log_in(self):
        response = self.client.post(self.url, self.form_input, follow = True)
        self.assertTrue(self.is_logged_in())
        response_url = reverse("feed")
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response,"feed.html")

    def test_successful_log_in_with_redirect(self):
        redirect_url = reverse("user_list")
        form_input = {"username": "@johndoe", "password": "Password123", "next" : redirect_url}
        response = self.client.post(self.url, form_input, follow = True)
        self.assertTrue(self.is_logged_in())
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response,"user_list.html")


    """Admins can make a user Active or Not, it is the equivalence of banning a user
    They should not be allowed to login because they are not active, even if thet have valid credentials
    Implmented by Deafult by Django"""
    def test_valid_log_in_by_inactive_user(self):
        self.user.is_active = False
        self.user.save()
        response = self.client.post(self.url, self.form_input)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,"log_in.html")
        form = response.context["form"]
        self.assertTrue(isinstance(form, LogInForm))  
        self.assertTrue(form.is_bound)
        self.assertFalse(self.is_logged_in())




    



