from django import forms
from microblogs.models import User
from django.core.validators import RegexValidator

class SignUpForms(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name","last_name","username","email","bio"]
        widgets = {"bio": forms.Textarea()}
    password = forms.CharField(
        label="password:",
        widget=forms.PasswordInput(),
        validators=[RegexValidator(
            regex=r'^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).*$',
            message='Password must contain an uppercase character, a lowercase character and a number' 
            )
        ]
    )
    passwordConfirmation = forms.CharField(label="Confirm Password:", widget=forms.PasswordInput())

    def clean(self):
        super().clean()
        password = self.cleaned_data.get("password")
        passwordConfirmation = self.cleaned_data.get("passwordConfirmation")
        if password != passwordConfirmation:
            self.add_error("passwordConfirmation", "Passwords do not match")
