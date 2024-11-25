from django.shortcuts import render, redirect, get_object_or_404
from users.decorators import role_required
from django.contrib.auth.decorators import login_required
from .models import Transaction
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.core import signing
from django.core.signing import BadSignature
from .models import Booking
from Movies.models import Show
from Food.models import Order, FoodItem

@login_required
@role_required(['regular',  'theateradmin'])
def view_transactions(request):
    user_profile = request.user.profile

    #  Retrieve transactions where the user is either the sender or the receiver
    transactions_withdraw = Transaction.objects.filter(
        sender_wallet=user_profile
    ).order_by('-timestamp')

    transactions_add = Transaction.objects.filter(
        receiver_wallet=user_profile
    ).order_by('-timestamp')

    return render(request,'Transactions/view_transactions.html',  {'transactions_withdraw': transactions_withdraw,  'transactions_add':transactions_add})

def initiate_refund(transaction):
    try:
        regular_user = transaction.sender_wallet
        theater_admin = transaction.receiver_wallet

        regular_user.wallet_balance += transaction.amount
        theater_admin.wallet_balance -= transaction.amount
        transaction.status = 'REVERTED'

        regular_user.save()
        theater_admin.save()
        transaction.save()

        return True

    except Exception as e:
        print(f"Refund failed: {e}")
        return False

def verify_otp(request,  token):
    try:
        data = signing.loads(token)
        source = data.get("source")  #  Decode and verify the token
        transaction_id = data.get("transaction_id")
    except BadSignature:
        messages.error(request,  "Invalid link.")
        return redirect("regular-dashboard")  #  Handle invalid token
    
    transaction = get_object_or_404(Transaction,  id=transaction_id)

    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        if entered_otp == transaction.otp:
            #  OTP is verified,  redirect based on the source
            if source == 'book_ticket':
                show_id = data.get("show_id")
                num_tickets = data.get("num_tickets")

                show = get_object_or_404(Show,  id=show_id)
                user_profile = request.user.profile
                theater_admin_profile = show.theater.admin.profile

                total_amount = num_tickets * show.ticket_price
                user_profile.wallet_balance -= total_amount
                theater_admin_profile.wallet_balance += total_amount
                user_profile.save()
                theater_admin_profile.save()

                #  Create a confirmed booking
                booking = Booking.objects.create(
                    user=request.user, 
                    show=show, 
                    status='CONFIRMED', 
                    tickets=num_tickets, 
                )

                show.booked_tickets += num_tickets
                show.save()

                transaction.status = 'COMPLETE'
                transaction.booking = booking
                transaction.save()

                send_mail(
                    'Virtual Bank Transaction Alert', 
                    f'Transaction summary:\nMovie: {show}\nNumber of tickets: {num_tickets}\nTotal Amount: {total_amount}\nType: Withdrawal\nBooked on: {booking.booking_date.strftime("%d-%m-%Y %H:%M")}', 
                    'settings.EMAIL_HOST_USER', 
                    [request.user.email, ], 
                    fail_silently=False, 
                )

                messages.success(request,  f"{num_tickets} tickets successfully booked for show {show}")
                return redirect('regular-dashboard')
            
            elif source == 'cancel_booking':
                booking = get_object_or_404(Booking, id=data.get("booking_id"))
                transaction_booking = get_object_or_404(Transaction, id=transaction_id)
                transaction_order = get_object_or_404(Transaction, id=data.get("transaction_order_id"))
                flag1 = initiate_refund(transaction_booking)
                flag2 = initiate_refund(transaction_order)
                if flag1 and flag2:
                    booking.status = 'CANCELLED'
                    booking.show.booked_tickets -= booking.tickets
                    booking.show.save()
                    booking.save()
                    send_mail(
                        'Virtual Bank Transaction Alert', 
                        f'Transaction summary:\nMovie: {booking.show}\nNumber of tickets: {num_tickets}\nTicket cancellation Amount: {transaction_booking.amount}\nFood Order cancellation amount: {transaction_order.booking}\nType: Refund\nBooked on: {booking.booking_date.strftime("%d-%m-%Y %H:%M")}\nNew balance: {request.user.profile.wallet_balance}', 
                        'settings.EMAIL_HOST_USER', 
                        [request.user.email, ], 
                        fail_silently=False, 
                    )
                    messages.success(request,  "The booking has been cancelled successfully,  and refund has been made.")
                else :
                    messages.error(request,  "Refund could not be completed.")
                return redirect('view-transactions')                   

            elif source == 'book_food':
                booking = get_object_or_404(Booking, id=data.get("booking_id"))
                
                food = get_object_or_404(FoodItem, id=data.get("food_id"))
                quantity = data.get("quantity")
                total_price = food.price * quantity

                user_profile = request.user.profile
                user_profile.wallet_balance -= total_price

                theater = booking.show.theater
                theater.admin.profile.wallet_balance += total_price
                user_profile.save()
                theater.admin.profile.save()

                order = Order.objects.create(
                    booking=booking, 
                    food_item=food, 
                    quantity=quantity, 
                    total_price=total_price
                )

                transaction.status = "COMPLETE"
                transaction.order = order
                transaction.save()

                send_mail(
                    'Transaction details', 
                    f'Transaction summary:\nMovie: {booking.show}\nFood Item: {food}\nTotal Amount: {total_price}\nType: Withdrawal\nBooked on: {order.ordered_at.strftime("%d-%m-%Y %H:%M")}\nNew balance: {user_profile.wallet_balance}', 
                    'settings.EMAIL_HOST_USER', 
                    [request.user.email, ], 
                    fail_silently=False, 
                )

                messages.success(request,  f"{food.name} ordered successfully! Transaction created.")
                return redirect('regular-dashboard')
            elif source == 'add_money':
                amount = data.get("amount")

                user_profile = request.user.profile
                user_profile.wallet_balance += amount
                user_profile.save()

                transaction.status = 'COMPLETE'
                transaction.save()

                send_mail(
                    'Wallet Recharge Successful', 
                    f'Your wallet has been credited with Rs.{amount}.\n New balance: {user_profile.wallet_balance}', 
                    'settings.EMAIL_HOST_USER', 
                    [request.user.email], 
                    fail_silently=False, 
                )

                messages.success(request,  f"₹{amount} has been added to your wallet.")
                return redirect('regular-dashboard')

        else:
            messages.error(request,  "Incorrect OTP entered. Please try again.")
    else:
        #  Send OTP email
        if source == 'book_ticket':
            show = get_object_or_404(Show,  id=data.get('show_id'))
            send_mail(
                'OTP for Booking Ticket', 
                f'Hi {request.user.username}, \nAn OTP has been requested for a transaction of Rs.{transaction.amount}.\n The OTP for booking the show for {show}: {transaction.otp}', 
                'settings.EMAIL_HOST_USER', 
                [request.user.email, ], 
                fail_silently=False, 
            )
        elif source == 'cancel_booking':
            booking = get_object_or_404(Booking, id=data.get("booking_id"))
            send_mail(
                'OTP for Cancelling Ticket', 
                f'Hi {request.user.username}, \nAn OTP has been requested for cancelling the booking of {booking.show}.\nThe OTP is {transaction.otp}', 
                'settings.EMAIL_HOST_USER', 
                [request.user.email, ], 
                fail_silently=False, 
            )
        elif source == 'book_food':
            send_mail(
                'OTP for Pre-Order', 
                f'Hi {request.user.username}. An OTP has been requested for a transaction of Rs.{transaction.amount}.\nThe OTP is {transaction.otp}', 
                'settings.EMAIL_HOST_USER', 
                [request.user.email, ], 
                fail_silently=False, 
            )
        elif source == 'add_money':
            amount = data.get("amount")
            send_mail(
                'OTP for Wallet Recharge', 
                f'Hi {request.user.username}, \nAn OTP has been requested for a wallet recharge of Rs.{amount}.\nThe OTP is {transaction.otp}', 
                'settings.EMAIL_HOST_USER', 
                [request.user.email], 
                fail_silently=False, 
            )

    return render(request,  'Transactions/verify_otp.html',  {'transaction': transaction})

def add_money(request):
    pass
