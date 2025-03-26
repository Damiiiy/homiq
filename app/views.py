from django.core.paginator import Paginator
from django.shortcuts import render, redirect

from property.models import House
from .forms import *
from .models import CustomUser

import random
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as lg
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

# Create your views here.


# login in views


def login_view(request):
    if request.user.is_authenticated:
        return redirect('profile')  # Redirect if already logged in

    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)

            if user is not None:
                auth_login(request, user)
                messages.success(request, 'Login successful!')
                return redirect('index')  # Redirect to profile or dashboard
            else:
                messages.error(request, 'Invalid email or password.')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomLoginForm()

    return render(request, 'accounts/login.html', {'form': form})




def login_auth(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data['username']  # Django's AuthenticationForm uses 'username'
            password = form.cleaned_data['password']

            print(f"Attempting login for: {email}")  # Debugging

            user = EmailAuthBackend.authenticate(request,  email=email, password=password)


            if user is not None:
                print("User authenticated successfully!")  # Debugging
                auth.login(request, user)
                messages.success(request, "Login successful!")

                # Redirect to the stored session URL or default dashboard
                next_url = request.session.pop('next', 'index')  # Remove session key
                return redirect(next_url)
            else:
                print("Authentication failed!")  # Debugging
                messages.error(request, "Invalid email or password.")
        else:
            print("Form validation errors:", form.errors)  # Debugging
            messages.error(request, "Please correct the errors below.")

    else:
        form = CustomLoginForm()

    return render(request, 'accounts/login.html', {'form': form})


# this is for the registration aspect
def register(request):
    form = RegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})


def registration_auth(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            try:
                new_user = CustomUser(
                    email=form.cleaned_data['email'],
                    name=form.cleaned_data['name'],
                    user_type=form.cleaned_data['user_type'],
                    password=form.cleaned_data['password1']
                )
                 # Hash the password before saving
                new_user.set_password(form.cleaned_data['password1'])
                new_user.save()
                # print(form.cleaned_data['name'])
                # user = form.save(commit=False)  # Create user instance without saving immediately
                # user.save()  # Save user instance
                messages.success(request, 'Registration Completed Successfully!')
                return redirect('register')  # Redirect to prevent form resubmission
            except ValidationError as e:
                for error in e.messages:
                    messages.error(request, error)  # Display Django's built-in validation errors
        else:
            # Loop through each field and add specific error messages
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")


    else:
        form = RegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})


def logout(request):
    lg(request)  # Logs out the user
    return redirect('login')

from property.forms import HouseForm
def userprofile(request):
    user = request.user
    form = HouseForm(user=user)

    houses = list(House.objects.filter(owner=user))  # Convert queryset to list for shuffling
    random.shuffle(houses)  # Shuffle the list to display random houses
    random_houses = houses[:5]
    paginator = Paginator(houses, 9)  # Show 9 houses per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'accounts/profile.html', {'user': user, 'form':form,'page_obj': page_obj, 'houses': random_houses})
