from django.db import models
from django.conf import settings

# Create your models here.
class BP(models.Model):
    systolic = models.IntegerField()
    diastolic = models.IntegerField()
    date = models.DateField(auto_now=False, auto_now_add=False)
    time = models.TimeField(auto_now=False, auto_now_add=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-date', '-time']

    def __str__(self):
        return f"{self.date}, {self.time}"
    

    # format=('%b %d, %Y')
    # format=('%I: %M')