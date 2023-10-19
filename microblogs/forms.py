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

    def save(self):
        super().save(commit=False)
        user = User.objects.create_user(
            username = self.cleaned_data.get("username"),
            first_name = self.cleaned_data.get("first_name"),
            last_name = self.cleaned_data.get("last_name"),
            email = self.cleaned_data.get("email"),
            bio = self.cleaned_data.get("bio"),
            password = self.cleaned_data.get("password")
        )
        return user
    

class LogInForm(forms.Form):
    username = forms.CharField(label="Username")
    password = forms.CharField(label="Password",widget=forms.PasswordInput())
