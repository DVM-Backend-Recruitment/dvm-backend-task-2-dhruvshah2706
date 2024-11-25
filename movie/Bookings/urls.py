from django.urls import path
from . import views

urlpatterns = [
    path('ticket/<int:show_id>', views.book_ticket, name='book-ticket'), 
    path('cancel/<int:booking_id>', views.cancel_booking, name='cancel-booking'), 
    path('food/<int:booking_id>', views.book_food, name='food-book')
]