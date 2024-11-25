from django.core.exceptions import PermissionDenied
from functools import wraps
from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden
from .models import Booking

def user_is_booking_owner(view_func):
    @wraps(view_func)
    def _wrapped_view(request,  booking_id,  *args,  **kwargs):
        #  Get the booking instance
        booking = get_object_or_404(Booking,  id=booking_id)
        
        #  Check if the logged-in user is the same as the one who made the booking
        if booking.user != request.user:
            return HttpResponseForbidden("You are not authorized to view or modify this booking.")
        
        return view_func(request,  booking_id,  *args,  **kwargs)
    
    return _wrapped_view
