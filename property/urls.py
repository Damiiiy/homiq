from django.urls import path
from .views import *


urlpatterns = [
    
    path('', index, name='index'),
    path('post-home/', create_house, name="post-house"),
    path('view-house/<int:id>/', view_house, name="view-house"),
    path('apply/<int:house_id>/',apply, name="apply"),
    path('properties/', all_houses, name="properties")
]