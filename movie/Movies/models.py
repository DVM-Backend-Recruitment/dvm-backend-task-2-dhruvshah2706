from django.db import models
from Theaters.models import Theater, Screen
from django.contrib.auth.models import User

class Movie(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    duration = models.IntegerField()  # Duration in minutes
    release_date = models.DateField()

    def __str__(self):
        return self.title

class Show(models.Model):
    movie = models.ForeignKey(Movie,  on_delete=models.CASCADE)
    theater = models.ForeignKey(Theater,  on_delete=models.CASCADE)
    screen = models.ForeignKey(Screen,  on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    ticket_price = models.DecimalField(max_digits=6,  decimal_places=2)
    booked_tickets = models.IntegerField(default=0)

    def available_seats(self):
        return self.screen.total_seats - self.booked_tickets
    
    def __str__(self):
        return self.movie.title
    

