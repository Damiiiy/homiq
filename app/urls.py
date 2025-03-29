from django.urls import path
from .views import *



urlpatterns = [
    # login/logout unit
    path('login/', login_view, name='login'),
    path('login-auth/', login_auth, name='auth'),
    path('logout/', logout, name='logout'),

    # registration unit
    path('register/', register, name='register'),
    path('reg-auth/', registration_auth, name='reg-auth'),
    # path('link_wallet_address', link_wallet_address, name='link_wallet_address'),


    # profile unit
    path('profile/', userprofile, name='profile')
]
