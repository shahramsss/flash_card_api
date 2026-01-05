from django.db import models
from django.utils import timezone


class Reminder(models.Model):
    title = models.CharField(max_length=512)
    start_day = models.DateField(default=timezone.localdate)
    one = models.BooleanField(default=False)
    two = models.BooleanField(default=False)
    seven = models.BooleanField(default=False)
    month = models.BooleanField(default=False)
    year = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} + {self.start_day}"
