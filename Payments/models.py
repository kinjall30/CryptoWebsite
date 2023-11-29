from django.db import models

# Create your models here.
class Wallet(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    userName = models.CharField(max_length=255)