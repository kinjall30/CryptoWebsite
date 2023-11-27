from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

print(settings.STRIPE_SECRET_KEY, settings.STRIPE_PUBLIC_KEY, "----------------------ttttt")

# def initializePayments(requests):
#     # 
#     return HttpResponse( "Hello World")


def payment_view(request):
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
            success_url=request.build_absolute_uri(f'success/'),
            cancel_url=request.build_absolute_uri('/cancel/'),

        )

        print(session, "---------------")
        return render(request, 'checkout.html', {"amount": amount, "paymentUrl": session.url })

    return render(request, 'payment_form.html')

def payment_success_view(request):
    if request.method == "GET":
        print(request.GET)
        return HttpResponse( "Hello World")
# Create your views here.
