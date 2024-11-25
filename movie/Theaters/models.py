from django.db import models
from django.contrib.auth.models import User

class Theater(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    admin = models.OneToOneField(User,  on_delete=models.CASCADE)  # Link to Theater Admin
    def __str__(self):
        return self.name

class Screen(models.Model):
    theater = models.ForeignKey(Theater,  on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    total_seats = models.IntegerField()

    def __str__(self):
        return self.name

