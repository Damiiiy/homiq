from django import forms
from django.contrib.auth import get_user_model
from .models import TYPE_CHOICES, House


class HouseForm(forms.ModelForm):
    name = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        help_text="Enter the house name."
    )

    mail = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        help_text="Optional. Enter a valid email."
    )
    location = forms.CharField(
        max_length=300,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        help_text="Enter the location."
    )

    phone = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        help_text="Optional. Enter a valid phone number."
    )

    address = forms.CharField(
        max_length=300,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        help_text="Enter the full address."
    )

    bedrooms = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        help_text="Optional. Enter the number of bedrooms."
    )

    bathrooms = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        help_text="Optional. Enter the number of bathrooms."
    )

    price = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        help_text="Optional. Enter the price in Naira."
    )

    # Owner will be set based on the authenticated user (hidden field)
    owner = forms.ModelChoiceField(
        queryset=get_user_model().objects.all(),  # Gets all users
        empty_label=None,
        required=False,
        widget=forms.HiddenInput()  # Hidden in the form, set programmatically
    )

    is_available = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        help_text="Check if the house is available."
    )

    type = forms.ChoiceField(
        choices=TYPE_CHOICES,
        required=True,
        widget=forms.Select(attrs={'class': 'form-select'}),
        help_text="Select the type of house."
    )

    description = forms.CharField(
        max_length=1000,
        required=True,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        help_text="Enter a brief description."
    )

    image = forms.ImageField(
        required=True,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'}),
        help_text="Optional. Upload an image of the house."
    )
    image2 = forms.ImageField(
        required=True,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'}),
        help_text="Optional. Upload an image of the house."
    )
    image3 = forms.ImageField(
        required=True,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'}),
        help_text="Optional. Upload an image of the house."
    )

    class Meta:
        model = House
        fields = [
            'name', 'mail', 'phone', 'address', 'bedrooms', 'bathrooms', 'price', 'location',
            'is_available', 'type', 'description', 'image', 'owner','image2','image3'
        ]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Get user from the view (for setting owner)
        super().__init__(*args, **kwargs)

        if user:
            self.fields['owner'].initial = user  # Set the owner field to the authenticated user

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price < 0:
            raise forms.ValidationError("Price cannot be negative.")
        return price

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone and not phone.isdigit():
            raise forms.ValidationError("Phone number should contain only digits.")
        return phone
