from django.db import models
from django.conf import settings

# Create your models here.
class Event(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='events'
    )
    image = models.CharField(max_length=5000)
    datetime = models.DateTimeField()
    location = models.CharField(max_length=500)

def __str__(self):
    return f"{self.datetime} @ {self.location}"