from django.test import TestCase
from microblogs.forms import LogInForm
from django.urls import reverse

"""Tests of the Log In View"""
class LogInViewTestCase(TestCase):


    def setUp(self):
        self.url = reverse("log_in")
        self.form_input = {
            "username" :"@johndow1",
            "password" : "UhDoe1",
        }


    def test_log_in_url(self):
        self.assertEquals(reverse("log_in"), "/log_in/")
    
    def test_get_log_in(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,"log_in.html")
        form = response.context["form"]
        self.assertTrue(isinstance(form, LogInForm))  
        self.assertFalse(form.is_bound)

    """ def test_unsuccessful_sign_up(self):
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
        self.assertTrue(is_password_correct) """


