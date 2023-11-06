from django.db import models
from django.conf import settings
from datetime import date

# Two date and time columns: same values but one for calculations and another for display 
class BP(models.Model):
    systolic = models.IntegerField()
    diastolic = models.IntegerField()
    date_num = models.DateField(auto_now=False, auto_now_add=False)
    date_str = models.DateField(auto_now=False, auto_now_add=False)
    time_num = models.TimeField(auto_now=False, auto_now_add=False)
    time_str = models.TimeField(auto_now=False, auto_now_add=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-date_num', '-time_num']

    def __str__(self):
        return f"{self.date_str}, {self.time_str}"
    
