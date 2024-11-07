from django.db import models
from django.utils import timezone

class Transaction(models.Model):
    sender_wallet = models.ForeignKey('users.Profile', on_delete=models.CASCADE, related_name='sent_transactions')
    receiver_wallet = models.ForeignKey('users.Profile', on_delete=models.CASCADE, related_name='received_transactions')
    transaction_type = models.CharField(max_length=20, choices=[('ticket', 'Ticket Booking'), ('food', 'Food Order')])
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=[('INCOMPLETE', 'Incomplete'), ('COMPLETE', 'Complete'), ('REVERTED', 'Reverted')])
    timestamp = models.DateTimeField(default=timezone.now)