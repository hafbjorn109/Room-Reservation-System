from django.db import models

# Create your models here.
class Room(models.Model):
    name = models.CharField(max_length=255)
    room_capacity = models.PositiveIntegerField()
    projector_availability = models.BooleanField()

class Reservation(models.Model):
    room_id = models.ForeignKey(Room, on_delete=models.CASCADE)
    date = models.DateField()
    comment = models.TextField(null=True)

    class Meta:
        unique_together = ('room_id', 'date')