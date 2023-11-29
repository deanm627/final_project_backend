from django.db import models
from django.conf import settings

# Two date and time columns: same values but one for calculations and another for display 
class Med(models.Model):
    name = models.CharField(max_length=255)
    dose = models.CharField(max_length=255)
    freq = models.CharField(max_length=255)
    start_date_num = models.DateField(auto_now=False, auto_now_add=False)
    start_date_str = models.DateField(auto_now=False, auto_now_add=False)
    end_date_num = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True)
    end_date_str = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True)
    assoc_medprob = models.CharField(max_length=255, blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-end_date_num', '-start_date_num']

    def __str__(self):
        return f"{self.name}"
    