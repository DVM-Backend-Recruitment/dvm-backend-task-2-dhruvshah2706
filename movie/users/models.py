from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Profile(models.Model):
    ROLE_CHOICES = [
        ('regular',  'Regular User'), 
        ('theateradmin',  'Theater Admin'), 
        ('superadmin',  'Super Admin'), 
    ]
    user = models.OneToOneField(User,  on_delete=models.CASCADE)
    role = models.CharField(max_length=20,  choices=ROLE_CHOICES,  default='regular')
    wallet_balance = models.DecimalField(max_digits=10,  decimal_places=2,  default=5000.00)

    def __str__(self):
        return f"{self.user.username} - {self.role} - Wallet: {self.wallet_balance}"
    

