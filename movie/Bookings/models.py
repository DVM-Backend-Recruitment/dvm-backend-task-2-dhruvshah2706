from django.db import models
from django.contrib.auth.models import User
from Movies.models import Show

class Booking(models.Model):
    user = models.ForeignKey(User,  on_delete=models.CASCADE)
    show = models.ForeignKey(Show,  on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10,  choices=[('PENDING',  'Pending'),  ('CONFIRMED',  'Confirmed'),  ('CANCELLED',  'Cancelled')])
    tickets = models.IntegerField(default=0)