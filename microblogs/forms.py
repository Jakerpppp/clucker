from django import forms
from microblogs.models import User
from django.core.validators import RegexValidator

class SignUpForms(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name","last_name","username","email","bio"]
        widgets = {"bio": forms.Textarea()}
    password = forms.CharField(
        label="Password:",
        widget=forms.PasswordInput(),
        validators = [
            RegexValidator(
                regex = r"[A-Z]", #any string that contains an upper case letter
                message = "Password must have at least one upper case character"
            ),
            RegexValidator(
                regex = r"[0-9]", #any string that contains a number
                message = "Password must have at least one upper case character"
            ),
            RegexValidator(
                regex = r"[a-z]", #any string that contains a lower case
                message = "Password must have at least one upper case character"
            ),

        ]
    )
    passwordConfirmation = forms.CharField(label="Confirm Password:", widget=forms.PasswordInput())

    def clean(self):
        super().clean()
        password = self.cleaned_data.get("password")
        passwordConfirmation = self.full_clean("passwordConfirmation")
        if password != passwordConfirmation:
            self.add_errors("passwordConfirmation", "Passwords do not match")
