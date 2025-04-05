from django.shortcuts import render, get_object_or_404, redirect
import random
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
from property.forms import HouseForm
from django.core.paginator import Paginator
from django.http import JsonResponse


# Create your views here.


def index(request):
    houses = list(House.objects.all())  # Get all houses as a list
    random.shuffle(houses)  # Shuffle the list randomly
    random_houses = houses[:5]  # Select 5 random houses (adjust as needed)

    return render(request, 'index.html', {'house': random_houses})

@login_required
def create_house(request):
    if request.method == 'POST':
        print(request.FILES)
        form = HouseForm(request.POST, request.FILES, user=request.user)
        # print( form )
        if form.is_valid():
            house = form.save(commit=False)
            house.owner = request.user
            house.save()
            messages.success(request, 'House created successfully!')
            return redirect('profile')
    else:
        form = HouseForm(user=request.user)

    return render(request, 'accounts/profile.html', {'form': form})


def view_house(request, id):
    house = get_object_or_404(House, id=id)
    return render(request, 'property/property-single.html', {'house': house})


@login_required(login_url='login')
def apply(request, house_id):

    house = get_object_or_404(House, id=house_id)
    user = request.user
    if AppliedHouses.objects.filter(house=house, user=user).exists():
        messages.warning(request, "You have already made reservations for this house.")
        return redirect('view-house', id=house_id)

    AppliedHouses.objects.create(house=house, user=user)
    # Send a success message
    messages.success(request, "You have successfully applied for this house!")
    return redirect('view-house', id=house_id)



def all_houses(request):
    houses = list(House.objects.all())
    random.shuffle(houses)
    random_houses = houses[:5]
    paginator = Paginator(houses, 9)  # Show 9 houses per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'property/properties.html', {'page_obj': page_obj, 'houses': random_houses})


def search(request):
    search_result = []  # Ensure 'search_result' is always defined

    if request.method == 'POST':
        keyword = request.POST.get('keyword', '').strip()  # Get and sanitize keyword
        if keyword:  # Only filter if keyword is provided
            search_result = list(House.objects.filter(location__icontains=keyword))  # Convert queryset to list

            random.shuffle(search_result)  # Shuffle results randomly

    # Pagination (only if there are search results)
    paginator = Paginator(search_result, 9)  # Show 9 houses per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    print(search_result)

    return render(request, 'property/search.html', {'houses': page_obj.object_list, 'page_obj': page_obj})