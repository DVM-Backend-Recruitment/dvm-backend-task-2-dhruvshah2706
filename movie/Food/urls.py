from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_food_item,  name='food-add'), 
    path('edit/<int:food_id>', views.edit_food_item,  name='food-edit'), 
    path('delete/<int:food_id>', views.delete_food_item,  name='food-delete'), 
]