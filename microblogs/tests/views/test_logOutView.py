from django.test import TestCase
from django.urls import reverse

from microblogs.models import User

from ..helpers import LogInTester

"""Tests of the Log Out View"""
class LogOutViewTestCase(TestCase, LogInTester):

    fixtures = ["microblogs/tests/fixtures/default_user.json"]

    def setUp(self):
        self.url = reverse("log_out")
        self.user = self.user = User.objects.get(username = "@janedoe")
        self.form_input = {
            "username" :"@janedoe",
            "password" : "Password123",
        }


    def test_log_in_url(self):
        self.assertEquals(reverse("log_out"), "/log_out/")

    def test_get_log_out(self):
        self.client.login(username="@janedoe", password = "Password123")
        self.assertTrue(self.is_logged_in())
        response = self.client.get(self.url, follow=True)
        response_url = reverse("home")
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response,"home.html")
        self.assertFalse(self.is_logged_in())
