from django.db import models
from django.utils import timezone
from users.models import Profile
from Bookings.models import Booking
from Food.models import Order

class Transaction(models.Model):
    sender_wallet = models.ForeignKey(Profile,  on_delete=models.CASCADE,  related_name='sent_transactions')
    receiver_wallet = models.ForeignKey(Profile,  on_delete=models.CASCADE,  related_name='received_transactions')
    transaction_type = models.CharField(max_length=20,  choices=[('ticket',  'Ticket Booking'),  ('food',  'Food Order')])
    amount = models.DecimalField(max_digits=10,  decimal_places=2)
    status = models.CharField(max_length=10,  choices=[('INCOMPLETE',  'Incomplete'),  ('COMPLETE',  'Complete'),  ('REVERTED',  'Reverted')])
    timestamp = models.DateTimeField(default=timezone.now)
    otp = models.CharField(max_length=6,  null=True,  blank=True)
    booking = models.ForeignKey(Booking,  on_delete=models.SET_NULL,  null=True,  blank=True,  related_name='transactions', default=None)
    order = models.ForeignKey(Order,  on_delete=models.SET_NULL,  null=True,  blank=True,  related_name='transactions', default=None)

    def __str__(self):
        return f"{self.transaction_type} - {self.amount} - {self.status}"
    