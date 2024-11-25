from django.db import models
from Theaters.models import Theater
from Bookings.models import Booking


class FoodItem(models.Model):
    theater = models.ForeignKey(Theater,  on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=5,  decimal_places=2)

    def __str__(self):
        return f'{self.name} - {self.price}'

class Order(models.Model):
    booking = models.ForeignKey(Booking,  on_delete=models.CASCADE)
    food_item = models.ForeignKey(FoodItem,  on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=6,  decimal_places=2)
    ordered_at = models.DateTimeField(auto_now_add=True)