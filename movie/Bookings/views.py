from django.shortcuts import render,  get_object_or_404,  redirect
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
from Food.models import Order, FoodItem
from .decorators import user_is_booking_owner
import random
from django.core import signing

def generate_otp():
    return f"{random.randint(100000,  999999)}"

@login_required
@role_required(['regular', ])
def book_ticket(request,  show_id):
    show = get_object_or_404(Show,  id=show_id)

    if timezone.now() > show.start_time:
        messages.error(request, "You can no longer book this show")
        return redirect('regular-dashboard')
    
    available_seats = show.available_seats()

    if request.method == 'POST':
        form = TicketBookingForm(request.POST)
        if form.is_valid():
            num_tickets = form.cleaned_data['num_tickets']
            total_amount = num_tickets * show.ticket_price

            #  Get the logged-in user's profile and theater admin's profile
            user_profile = request.user.profile
            theater_admin_profile = show.theater.admin.profile

            #  Check if the user has enough wallet balance
            if user_profile.wallet_balance >= total_amount:
                #  Deduct money from user's wallet and add it to theater admin's wallet
                otp = generate_otp()
                transaction = Transaction.objects.create(
                    sender_wallet=user_profile, 
                    receiver_wallet=theater_admin_profile, 
                    transaction_type='ticket', 
                    amount=total_amount, 
                    status='PENDING',  #  when transaction is not yet complete
                    otp=otp
                )
                data = {
                    "transaction_id": transaction.id, 
                    "source": "book_ticket", 
                    "show_id": show_id, 
                    "num_tickets": num_tickets
                }
                token = signing.dumps(data)
                return redirect('verify-otp',  token=token)

            else:
                #  Insufficient funds,  revert the changes
                Transaction.objects.create(
                    
                    sender_wallet=user_profile, 
                    receiver_wallet=theater_admin_profile, 
                    transaction_type='ticket', 
                    amount=total_amount, 
                    status='INCOMPLETE'
                )

                messages.error(request,  "Insufficient funds. Please add money to your wallet.")
                return redirect('book-ticket', show_id=show_id)  #  Or display an error page

    else:
        form = TicketBookingForm()

    context = {
        'show': show, 
        'form': form, 
        'available_seats': available_seats, 
    }

    return render(request,  'Bookings/book_ticket.html',  context)

@login_required
@role_required(['regular', ])
@user_is_booking_owner
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking,  id=booking_id)
    if timezone.now() > booking.show.start_time:
        messages.error(request, "You can no longer cancel this booking")
        return redirect('view-transactions')

    if request.method == 'POST':
        # If it's a POST request,  delete the screen
        transaction_booking = Transaction.objects.get(booking=booking)
        order = Order.objects.get(booking=booking)
        transaction_order = Transaction.objects.get(order=order)
        otp = generate_otp()
        transaction_booking.otp = otp
        transaction_booking.save()
        data = {
            "transaction_id": transaction_booking.id, 
            "transaction_order_id": transaction_order.id, 
            "source": "cancel_booking", 
            "booking_id": booking.id, 
        }
        token = signing.dumps(data)
        return redirect('verify-otp',  token=token)

        flag1 = initiate_refund(transaction_booking)
        flag2 = initiate_refund(transaction_order)
        if flag1 and flag2:
            booking.status = 'Cancelled'
            booking.show.booked_tickets -= booking.tickets
            booking.show.save()
            booking.save()
            messages.success(request,  "The booking has been cancelled successfully,  and refund has been made.")
        else :
            messages.error(request,  "Refund could not be completed.")
        return redirect('view-transactions')
    
    return render(request,  'Bookings/booking_cancel.html',  {'booking': booking})

@login_required
@role_required(['regular'])
@user_is_booking_owner
def book_food(request,  booking_id):
    booking = get_object_or_404(Booking,  id=booking_id,  user=request.user)
    if timezone.now() > booking.show.start_time:
        messages.error(request, "You can no longer order for this show")
        return redirect('regular-dashboard')
    theater = booking.show.theater
    user_profile = request.user.profile  #  Assuming a profile is linked to the user

    if booking.status == "Cancelled" or booking.status == "CANCELLED":
        messages.error(request, "Cannot pre-book food orders for cancelled booking")
        return redirect('regular-dashboard')
    if request.method == 'POST':
        form = FoodOrderForm(request.POST,  theater=theater)
        if form.is_valid():
            food = form.cleaned_data['food_item']
            quantity = form.cleaned_data['quantity']
            total_price = food.price * quantity
            if user_profile.wallet_balance >= total_price:
                otp = generate_otp()
                transaction = Transaction.objects.create(
                    sender_wallet=user_profile, 
                    receiver_wallet=theater.admin.profile, 
                    transaction_type='food', 
                    amount=total_price, 
                    status='PENDING',  #  when transaction is not yet complete
                    otp=otp
                )
                data = {
                    "transaction_id": transaction.id, 
                    "source": "book_food", 
                    "booking_id": booking_id, 
                    "food_id": food.id, 
                    "quantity": quantity
                }
                token = signing.dumps(data)
                return redirect('verify-otp',  token=token)

                # user_profile.wallet_balance -= total_price
                # theater.admin.profile.wallet_balance += total_price

                # user_profile.save()
                # theater.admin.profile.save()

                # order = Order.objects.create(
                #     booking=booking, 
                #     food_item=food_item, 
                #     quantity=quantity, 
                #     total_price=total_price, 
                #     ordered_at=timezone.now()
                # )

                # Transaction.objects.create(
                #     sender_wallet=user_profile, 
                #     receiver_wallet=theater.admin.profile, 
                #     transaction_type='food', 
                #     amount=total_price, 
                #     status='COMPLETE', 
                #     order = order
                # )

                # messages.success(request,  f"{food_item.name} ordered successfully! Transaction created.")
                # return redirect('regular-dashboard')
            
            else:
                messages.error(request,  "Insufficient balance! Order could not be placed.")
                return redirect('regular-dashboard')
    else:
        form = FoodOrderForm(theater=theater)

    return render(request,  'Bookings/book_food.html',  {'form': form,  'booking': booking})

