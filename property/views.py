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
        messages.warning(request, "You have already applied for this house.")
        return redirect('view-house', id=house_id)

    AppliedHouses.objects.create(house=house, user=user)
    # Send a success message
    messages.success(request, "You have successfully applied for this house!")
    return redirect('view-house', id=house_id)



# def search_houses(request):
#     query = request.GET.get('query', '')
#     price = request.GET.get('price', '')
#     bedrooms = request.GET.get('bedrooms', '')
#     bathrooms = request.GET.get('bathrooms', '')
#     location = request.GET.get('location', '')
#
#     houses = House.objects.all()
#
#     if query:
#         houses = houses.filter(title__icontains=query)
#     if price:
#         houses = houses.filter(price__lte=price)  # Less than or equal to the price
#     if bedrooms:
#         houses = houses.filter(bedrooms__gte=bedrooms)  # At least the specified number of bedrooms
#     if bathrooms:
#         houses = houses.filter(bathrooms__gte=bathrooms)  # At least the specified number of bathrooms
#     if location:
#         houses = houses.filter(location__icontains=location)  # Partial match for location
#
#     results = [
#         {
#             "id": house.id,
#             "title": house.title,
#             "image": house.image.url,
#             "price": house.price,
#             "bedrooms": house.bedrooms,
#             "bathrooms": house.bathrooms,
#             "location": house.location,
#         }
#         for house in houses[:5]  # Limit results to 5
#     ]
#
#     return JsonResponse(results, safe=False)

def all_houses(request):
    houses = list(House.objects.all())
    random.shuffle(houses)
    random_houses = houses[:5]
    paginator = Paginator(houses, 9)  # Show 9 houses per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'property/properties.html', {'page_obj': page_obj, 'houses': random_houses})

# def search(request):
#     if request.method == 'POST':
#         keyword = request.POST.get('keyword')
#
#         search = House.objects.filter(location__icontains=keyword)
#
#     # houses = list(House.objects.all())  # Get all houses as a list
#     # random.shuffle(houses)  # Shuffle the list randomly
#     # selected_houses = houses[:3]  # Select the first 3 houses from the shuffled list
#     return render(request, 'property/search.html',  {'houses': search })


# def search(request):
#     search_result = []  # Ensure 'search' is always defined
#
#     random.shuffle(search_result)
#     random_houses = search_result[:5]
#     paginator = Paginator(search_result, 9)  # Show 9 houses per page
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#
#
#     if request.method == 'POST':
#         keyword = request.POST.get('keyword', '').strip()  # Get and sanitize keyword
#         if keyword:  # Only filter if keyword is provided
#             search_result = House.objects.filter(location__icontains=keyword)  # Fixed typo
#
#     return render(request, 'property/search.html', {'houses': search_result, 'page_obj': page_obj })


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