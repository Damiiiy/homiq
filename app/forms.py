from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser




choices_of_user = (("seeker", "Home Seeker"),("owner", "House Owner"))
class RegistrationForm(UserCreationForm):
    email = forms.EmailField(
        label="Full Name",
        max_length=50,
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email'}),
        help_text="Enter your email address."
    )

    name = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder' : 'Full name'
        }),
        help_text="Optional."
    )
    user_type = forms.ChoiceField(
        choices=choices_of_user,
        widget=forms.Select(attrs={
            'class': 'form-control',
            }),
        label="I am a"
    )
    password1 = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder' : 'Enter Password'
        }),
        help_text="Optional."
    )
    password2 = forms.CharField(
            max_length=100,
            required=True,
            widget=forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder' : 'Confirm Password'
            }),
            help_text="Optional."
        )

    class Meta:
        model = CustomUser
        fields = ['email', 'password1', 'password2', 'user_type']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = self.cleaned_data['user_type']
        if commit:
            user.save()
        return user


class CustomLoginForm(AuthenticationForm):
    username = forms.EmailField(
            widget=forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your email',
                'autofocus': True,
            }),
    )
    password = forms.CharField(
            widget=forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your password',
            }),
        )