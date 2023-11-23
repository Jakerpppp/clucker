from django import forms
from microblogs.models import User, Post
from django.core.validators import RegexValidator
from django.contrib.auth import authenticate

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


    def get_user(self):
        '''Returns True if the User is Valid'''
        user = None
        if self.is_valid():
            username = self.cleaned_data.get("username")
            password = self.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
        return user

"""Form to ask user for post text. The post author must be by the post creator.
    """
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['text']
        widgets = {
            'text': forms.Textarea()
        }

class UserForm(forms.ModelForm):
    """Form to update user profiles."""

    class Meta:
        """Form options."""

        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'bio']
        widgets = { 'bio': forms.Textarea() }

class PasswordForm(forms.Form):
    """Form enabling users to change their password."""

    password = forms.CharField(label='Current password', widget=forms.PasswordInput())
    new_password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(),
        validators=[RegexValidator(
            regex=r'^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).*$',
            message='Password must contain an uppercase character, a lowercase '
                    'character and a number'
            )]
    )
    password_confirmation = forms.CharField(label='Password confirmation', widget=forms.PasswordInput())

    def clean(self):
        """Clean the data and generate messages for any errors."""

        super().clean()
        new_password = self.cleaned_data.get('new_password')
        password_confirmation = self.cleaned_data.get('password_confirmation')
        if new_password != password_confirmation:
            self.add_error('password_confirmation', 'Confirmation does not match password.')

