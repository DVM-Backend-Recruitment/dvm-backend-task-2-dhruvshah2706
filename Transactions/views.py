from django.shortcuts import render
from users.decorators import role_required
from django.contrib.auth.decorators import login_required
from .models import Transaction


@login_required
@role_required(['regular', 'theateradmin'])
def view_transactions(request):
    user_profile = request.user.profile

    # Retrieve transactions where the user is either the sender or the receiver
    transactions_withdraw = Transaction.objects.filter(
        sender_wallet=user_profile
    ).order_by('-timestamp')

    transactions_add = Transaction.objects.filter(
        receiver_wallet=user_profile
    ).order_by('-timestamp')

    return render(request, 'transactions/view_transactions.html', {'transactions_withdraw': transactions_withdraw, 'transactions_add':transactions_add})

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

