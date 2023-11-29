from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from .models import Wallet
from decimal import Decimal
import stripe
from django.contrib.auth.decorators import login_required

stripe.api_key = settings.STRIPE_SECRET_KEY

print(settings.STRIPE_SECRET_KEY, settings.STRIPE_PUBLIC_KEY, "----------------------ttttt")

# def initializePayments(requests):
#     # 
#     return HttpResponse( "Hello World")

@login_required
def payment_view(request):
    username =request.user.username
    if request.method == 'POST':
        amount = request.POST['amount']

        # create checkout session
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': 'Your Product',
                    },
                    'unit_amount': int(float(amount) * 100),  # Convert to cents
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=request.build_absolute_uri(f'success/?user={username}&amount={amount}'),
            cancel_url=request.build_absolute_uri('/cancel/'),

        )


        print(session, "---------------")
        return render(request, 'checkout.html', {"amount": amount, "paymentUrl": session.url })

    return render(request, 'payment_form.html')

@login_required
def payment_success_view(request):
    if request.method == "GET":
        username = request.user.username
        amount = Decimal(request.GET.get('amount', '0.0'))

        # Check if Wallet entry with the given userName exists
        wallet_entry, created = Wallet.objects.get_or_create(userName=username, defaults={'amount': amount})

        if not created:
            total =  wallet_entry.amount + amount
            wallet_entry.amount = wallet_entry.amount + amount
            wallet_entry.save()
        
            return HttpResponse(str(total))

        print(request.GET, username)
        return HttpResponse(str(amount))
# Create your views here.
