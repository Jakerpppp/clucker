from django.test import TestCase
from django.urls import reverse
from microblogs.forms import SignUpForms
from microblogs.models import User
from django.contrib.auth.hashers import check_password
from django import forms

class SignUpFormsTestCase(TestCase):
    
    def setUp (self):
        self.form_input = {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'username': '@janedoe',
            'email': 'janedoe@example.org',
            'bio': 'Jane Doe is also a talking head',
            'password': 'Password123',
            'passwordConfirmation': 'Password123'
        }

    def test_valid_sign_up_form(self):
        form = SignUpForms(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_has_necessary_fields(self):
        form = SignUpForms()
        self.assertIn('first_name', form.fields) 
        self.assertIn('last_name', form.fields) 
        self.assertIn('username', form.fields) 
        self.assertIn ('email', form.fields)
        email_field = form.fields['email']
        self.assertTrue(isinstance (email_field, forms.EmailField)) 
        self.assertIn('bio', form.fields) 
        self.assertIn('password', form.fields)
        password_widget = form.fields['password'].widget
        self.assertTrue (isinstance (password_widget, forms.PasswordInput)) 
        self.assertIn('passwordConfirmation', form.fields)
        passwordConfirmation_widget = form.fields['passwordConfirmation'].widget
        self. assertTrue(isinstance(passwordConfirmation_widget, forms.PasswordInput))

    def test_form_uses_model_validation(self):
        self.form_input[ 'username'] = 'badusername'
        form = SignUpForms(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_password_must_contain_uppercase_character(self):
        self.form_input[ 'password'] = 'password123'
        self.form_input['passwordConfirmation'] = 'password123'
        form = SignUpForms(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_password_must_contain_lowercase_character(self):
        self.form_input['password'] = 'PASSWORD123'
        self.form_input['passwordConfirmation'] = 'PASSWORD123'
        form = SignUpForms(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_password_must_contain_number(self):
        self.form_input['password'] = 'PasswordABC'
        self.form_input['passwordConfirmation'] = 'PasswordABC'
        form = SignUpForms(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_password_and_passwordConfirmation_are_identical(self):
        self.form_input['passwordConfirmation'] = 'WrongPassword123'
        form = SignUpForms (data=self.form_input)
        self.assertFalse(form.is_valid ())

    def test_form_must_save_correctly(self):
        form = SignUpForms (data=self.form_input)
        before_count = User.objects.count()
        form.save()
        after_count = User.objects.count()
        self.assertEquals(before_count+1,after_count)
        user = User.objects.get(username="@janedoe")
        self.assertEqual(user.first_name, "Jane")
        self.assertEqual(user.last_name, "Doe")
        self.assertEqual(user.email, "janedoe@example.org")
        self.assertEqual(user.bio, "Jane Doe is also a talking head")
        is_password_correct = check_password("Password123", user.password)
        self.assertTrue(is_password_correct)


    

