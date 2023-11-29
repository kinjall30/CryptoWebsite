from django.contrib import admin
from .models import UserDetails, Transactions, Coin, UserProfile, UserIdentity, HistoricalPrice, TrendingCrypto, CryptoAsset

admin.site.register(UserDetails)
admin.site.register(UserIdentity)
admin.site.register(HistoricalPrice)
admin.site.register(TrendingCrypto)
admin.site.register(CryptoAsset)
admin.site.register(UserProfile)
admin.site.register(Coin)
admin.site.register(Transactions)
admin.site.register(CryptoAsset)
