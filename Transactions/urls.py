from django.urls import path
from . import views

urlpatterns = [
    path('view/', views.view_transactions,name = 'view-transactions'),
]