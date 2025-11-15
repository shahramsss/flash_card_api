from django.db import models

class Reminder(models.Model):
    title = models.CharField(max_length=512)
    start_day = models.DateField(auto_now_add=True)
    one= models.DateField()
    two= models.DateField()
    seven= models.DateField()
    month = models.DateField()
    year = models.DateField()
    
    def __str__(self):
        return f"{self.title} + {self.start_day}"

