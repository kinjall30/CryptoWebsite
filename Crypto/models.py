from django.db import models

class UserDetails(models.Model):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255,null=True, blank=True)
    first_name = models.CharField(max_length=255, null = True, blank=True)
    last_name = models.CharField(max_length=255, null = True, blank=True)
    date_of_birth = models.DateField(blank=True, null = True)

class HistoricalPrice(models.Model):
    cryptocurrency = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=20, decimal_places=5)
    date = models.DateField()

    def __str__(self):
        return self.username
class CryptoAsset(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=20, decimal_places=5)
    high = models.DecimalField(max_digits=20, decimal_places=5, null=True, blank=True)
    low = models.DecimalField(max_digits=20, decimal_places=5, null=True, blank=True)
    price_change_24h = models.DecimalField(max_digits=20, decimal_places=5, null=True, blank=True)
    price_change_percentage_24h = models.DecimalField(max_digits=20, decimal_places=5, null=True, blank=True)
    market_cap = models.DecimalField(max_digits=20, decimal_places=5, null=True, blank=True)
    volume_24h = models.DecimalField(max_digits=20, decimal_places=5, null=True, blank=True)
    circulating_supply = models.DecimalField(max_digits=20, decimal_places=5, null=True, blank=True)

    def __str__(self):
        return self.name