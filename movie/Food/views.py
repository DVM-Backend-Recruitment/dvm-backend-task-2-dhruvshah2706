from django.shortcuts import render, redirect, get_object_or_404
from .forms import AddFoodItemForm
from Theaters.models import Theater
from .models import FoodItem
from django.contrib.auth.decorators import login_required
from .decorators import is_theater_admin
from django.contrib import messages
from users.decorators import role_required

@login_required
@role_required(['theateradmin', ])
def add_food_item(request):
    theater = Theater.objects.get(admin=request.user)
    if request.method == 'POST':
        food_form = AddFoodItemForm(request.POST)
        if food_form.is_valid():
            food = food_form.save(commit=False)
            food.theater = theater
            food.save()
            return redirect('theater-dashboard', pk=theater.pk)
    else:
        food_form = AddFoodItemForm()

    return render(request,  'Food/add_food_item.html',  {'food_form': food_form, 'theater':theater})

@login_required
@is_theater_admin
def edit_food_item(request,  food_id):
    food = get_object_or_404(FoodItem,  id=food_id)

    if request.method == 'POST':
        food_form = AddFoodItemForm(request.POST,  instance=food)
        if food_form.is_valid():
            food = food_form.save()
            return redirect('theater-dashboard',  pk=food.theater.pk)  # Redirect to theater detail page
    else:
        food_form = AddFoodItemForm(instance=food)

    return render(request,  'Food/edit_food_item.html',  {'food_form': food_form,  'food': food})

@login_required
@is_theater_admin
def delete_food_item(request,  food_id):
    food = get_object_or_404(FoodItem,  id=food_id)

    if request.method == 'POST':
        food.delete()
        messages.success(request,  "The screen has been deleted successfully.")
        return redirect('theater-dashboard',  pk=food.theater.pk)  # Redirect back to the theater details page
    
    return render(request,  'Food/food_confirm_delete.html',  {'food': food})




        

