from django import forms

from microblogs.models import User

class SignUpForms(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name","last_name","username","email","bio"]
        widgets = {"bio": forms.Textarea()}
    password = forms.CharField(label="Password:", widget=forms.PasswordInput())
    passwordConfirmation = forms.CharField(label="Confirm Password:", widget=forms.PasswordInput())
