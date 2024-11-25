from django.contrib import admin
from django.urls import path,  include
from users import views as users_views
from Transactions import views as transactions_views
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/',  admin.site.urls), 
    path('login/',  users_views.custom_login,  name='login'), 
    path('logout/',  users_views.custom_logout,  name='logout'), 
    path('dashboard/',  users_views.regular_dashboard,  name='regular-dashboard'), 
    path('',  RedirectView.as_view(url='/dashboard/', permanent=False), name='home'), 
    path('accounts/login/',  RedirectView.as_view(url='/login/',  permanent=False)), 
    path('accounts/',  include('allauth.urls')), 
    path('theater/', include('Theaters.urls')), 
    path('show/', include('Movies.urls')), 
    path('food/', include('Food.urls')), 
    path('profile/', users_views.profile, name='profile'), 
    path('booking/', include('Bookings.urls')), 
    path('transactions/', include('Transactions.urls')), 
    path('profile/', users_views.profile, name='profile'), 
    path('verify_otp/<str:token>/', transactions_views.verify_otp, name='verify-otp')
]