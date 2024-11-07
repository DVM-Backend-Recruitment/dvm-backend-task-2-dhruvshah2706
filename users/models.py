from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Profile(models.Model):
    ROLE_CHOICES = [
        ('regular', 'Regular User'),
        ('theateradmin', 'Theater Admin'),
        ('superadmin', 'Super Admin'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='regular')
    wallet_balance = models.DecimalField(max_digits=10, decimal_places=2, default=500.00)

    def __str__(self):
        return f"{self.user.username} - {self.role} - Wallet: {self.wallet_balance}"
    
class WalletTransaction(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=20, choices=[('add', 'Add'), ('withdraw', 'Withdraw')])
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=[('INCOMPLETE', 'Incomplete'), ('COMPLETE', 'Complete'), ('REVERTED', 'Reverted')])
    timestamp = models.DateTimeField(default=timezone.now)
