from django.test import TestCase
from django import forms
from microblogs.forms import LogInForm

"""Unit Tests of the Log In Form"""
class LogInFormTestCase(TestCase):

    def setUp(self):
        self.form_input = {"username": "@johnDoe", "password": "Password123"}
    
    def test_form_has_required_fields(self):
        form = LogInForm()
        self.assertIn("username", form.fields)
        self.assertIn("password", form.fields)
        password_field = form.fields["password"]
        self.assertTrue(isinstance(password_field.widget, forms.PasswordInput)) #The widget used for the password is a password Input widget

    def test_form_accepts_valid_input(self):
        form = LogInForm(data=self.form_input)
        self.assertTrue(form.is_valid())
    
    """This is so the user cannot get any hints when trying to log in"""
    def test_form_accepts_invalid_username(self):
        self.form_input["username"] = "Hello"
        form = LogInForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_accepts_invalid_password(self):
        self.form_input["password"] = "Hello"
        form = LogInForm(data=self.form_input)
        self.assertTrue(form.is_valid())


    def test_form_rejects_blank_username(self):
        self.form_input["username"] = ""
        form = LogInForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_rejects_blank_password(self):
        self.form_input["password"] = ""
        form = LogInForm(data=self.form_input)
        self.assertFalse(form.is_valid())



