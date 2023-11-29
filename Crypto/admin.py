from django.contrib import admin
from .models import UserDetails,UserIdentity, Transactions

admin.site.register(UserDetails)
admin.site.register(UserIdentity)
admin.site.register(Transactions)
