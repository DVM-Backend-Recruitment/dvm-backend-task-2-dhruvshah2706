from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404
from .models import FoodItem


def is_theater_admin(view_func):
    def _wrapped_view(request,  *args,  **kwargs):
        food = get_object_or_404(FoodItem,  id=kwargs['food_id'])
        if food.theater.admin != request.user:
            return HttpResponseForbidden('You do not have permission to edit this food.')
        return view_func(request,  *args,  **kwargs)
    return _wrapped_view