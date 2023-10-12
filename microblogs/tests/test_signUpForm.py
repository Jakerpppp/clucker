from django.test import TestCase
from microblogs.forms import SignUpForms
from microblogs.models import User

class SignUpFormTestCase(TestCase):
    
    def test_valid_input_data(self):
        form_input = {
            "first_name" : "John",
            "last_name" : "Doe",
            "username" :"@johndow1",
            "email" : "johndoe@gmail.com",
            "bio" : "John Doe is a talking head",
            "password" : "UhDoe",
            "passwordConfirmation" : "UhDoe"
        }
        form = SignUpForms(data=form_input)
        print(form.errors)
        self.assertTrue(form.is_valid())
        #Example of a Test

    

