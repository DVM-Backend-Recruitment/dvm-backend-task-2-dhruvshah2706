#  Generated by Django 5.1 on 2024-11-11 15:37

from django.db import migrations,  models


class Migration(migrations.Migration):

    dependencies = [
        ('Movies',  '0003_delete_booking'), 
    ]

    operations = [
        migrations.AddField(
            model_name='show', 
            name='booked_tickets', 
            field=models.IntegerField(default=0), 
        ), 
    ]