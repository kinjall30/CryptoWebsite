from django.db import models

# Create your models here.
def Payment():
    amount = models.DecimalField(max_digits=10, decimal_places=2)