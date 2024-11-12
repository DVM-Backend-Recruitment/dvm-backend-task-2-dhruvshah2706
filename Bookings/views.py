from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Booking
from Movies.models import Show
from Transactions.models import Transaction
from .forms import TicketBookingForm
from users.decorators import role_required
from django.contrib.auth.decorators import login_required
from Transactions.views import initiate_refund
from django.utils import timezone
from .forms import FoodOrderForm
from Food.models import Order
from .decorators import user_is_booking_owner


def book_ticket(request, show_id):
    show = get_object_or_404(Show, id=show_id)

    if timezone.now() > show.start_time:
        messages.error(request,"You can no longer book this show")
        return redirect('regular-dashboard')
    
    available_seats = show.available_seats()

    if request.method == 'POST':
        form = TicketBookingForm(request.POST)
        if form.is_valid():
            num_tickets = form.cleaned_data['num_tickets']
            total_amount = num_tickets * show.ticket_price

            # Get the logged-in user's profile and theater admin's profile
            user_profile = request.user.profile
            theater_admin_profile = show.theater.admin.profile

            # Check if the user has enough wallet balance
            if user_profile.wallet_balance >= total_amount:
                # Deduct money from user's wallet and add it to theater admin's wallet
                user_profile.wallet_balance -= total_amount
                theater_admin_profile.wallet_balance += total_amount
                user_profile.save()
                theater_admin_profile.save()

                # Create a confirmed booking
                booking = Booking.objects.create(
                    user=request.user,
                    show=show,
                    status='CONFIRMED',
                    tickets = num_tickets,
                )

                # Create a successful transaction
                Transaction.objects.create(
                    sender_wallet=user_profile,
                    receiver_wallet=theater_admin_profile,
                    transaction_type='ticket',
                    amount=total_amount,
                    status='COMPLETE',
                    booking = booking
                )

                

                show.booked_tickets += num_tickets
                show.save()

                messages.success(request, f"{num_tickets} tickets successfully booked!")
                return redirect('regular-dashboard')

            else:
                # Insufficient funds, revert the changes
                Transaction.objects.create(
                    sender_wallet=user_profile,
                    receiver_wallet=theater_admin_profile,
                    transaction_type='ticket',
                    amount=total_amount,
                    status='INCOMPLETE'
                )

                messages.error(request, "Insufficient funds. Please add money to your wallet.")
                return redirect('book-ticket',show_id=show_id)  # Or display an error page

    else:
        form = TicketBookingForm()

    context = {
        'show': show,
        'form': form,
        'available_seats': available_seats,
    }

    return render(request, 'Bookings/book_ticket.html', context)

@login_required
@role_required(['regular',])
def cancel_booking(request,booking_id):
    
    booking = get_object_or_404(Booking, id=booking_id)
    if timezone.now() > booking.show.start_time:
        messages.error(request,"You can no longer cancel this booking")
        return redirect('view-transactions')

    if request.method == 'POST':
        #If it's a POST request, delete the screen
        transaction = Transaction.objects.get(booking=booking)
        flag = initiate_refund(transaction)
        if flag:
            booking.status = 'Cancelled'
            booking.show.booked_tickets -= booking.tickets
            booking.show.save()
            booking.save()
            messages.success(request, "The booking has been cancelled successfully.")
        else:
            messages.error(request, "Refund could not be completed.")
        return redirect('view-transactions')
    
    return render(request, 'Bookings/booking_cancel.html', {'booking': booking})

@login_required
@role_required(['regular'])
@user_is_booking_owner
def book_food(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    theater = booking.show.theater
    user_profile = request.user.profile  # Assuming a profile is linked to the user

    if booking.status == "Cancelled" or booking.status == "CANCELLED":
        messages.error("Cannot pre-book food orders for cancelled booking")
        return redirect('regular-dashboard')
    if request.method == 'POST':
        form = FoodOrderForm(request.POST, theater=theater)
        if form.is_valid():
            food_item = form.cleaned_data['food_item']
            quantity = form.cleaned_data['quantity']
            total_price = food_item.price * quantity
            if user_profile.wallet_balance >= total_price:
                user_profile.wallet_balance -= total_price
                theater.admin.profile.wallet_balance += total_price

                user_profile.save()
                theater.admin.profile.save()

                order = Order.objects.create(
                    booking=booking,
                    food_item=food_item,
                    quantity=quantity,
                    total_price=total_price,
                    ordered_at=timezone.now()
                )

                Transaction.objects.create(
                    sender_wallet=user_profile,
                    receiver_wallet=theater.admin.profile,
                    transaction_type='food',
                    amount=total_price,
                    status='COMPLETE',
                    timestamp=timezone.now(),
                    order = order
                )

                messages.success(request, f"{food_item.name} ordered successfully! Transaction created.")
                return redirect('regular-dashboard')
            
            else:
                messages.error(request, "Insufficient balance! Order could not be placed.")
                return redirect('regular-dashboard')
    else:
        form = FoodOrderForm(theater=theater)

    return render(request, 'Bookings/book_food.html', {'form': form, 'booking': booking})

