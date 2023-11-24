# views.py
import requests
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignUpForm, LoginForm
from .models import UserDetails
from .models import UserDetails, Coin
from django.http import HttpResponseServerError

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('CryptoCrackers:login')
    else:
        form = SignUpForm()
    return render(request, 'sigup.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            try:
                user = UserDetails.objects.get(username=username)
                if user.password == password:
                    # Dhruvesh please use this session id or username to get user-data.
                    request.session['user_id'] = user.id
                    request.session['username'] = user.username

                    # messages.success(request, f'Welcome back, {username}!')
                    return redirect('CryptoCrackers:index')  # Redirect to a home page or dashboard
                else:
                    messages.error(request, 'Password is incorrect.')
            except UserDetails.DoesNotExist:
                messages.error(request, 'Username does not exist.')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def index(request):
    return render(request, 'base.html')

def portfolio(request):
    return render(request, 'portfolio.html')

def watchlist(request):
    try:
        # Fetch data from CoinGecko API
        api_url = 'https://api.coingecko.com/api/v3/coins/markets'
        params = {
            'vs_currency': 'usd',
            'order': 'market_cap_desc',
            'per_page': 10,
            'page': 1,
            'sparkline': False,
        }

        response = requests.get(api_url, params=params)
        response.raise_for_status()  # Raise an exception for bad responses (4xx and 5xx)

        coins_data = response.json()

        # Save the data to the database (update or create)
        for coin_data in coins_data:
            try:
                # Check if 'id' is a valid numerical value
                coin_id = int(coin_data['id'])
            except ValueError:
                # Skip entries with invalid 'id'
                continue

            Coin.objects.update_or_create(
                id=coin_id,
                defaults={
                    'name': coin_data['name'],
                    'symbol': coin_data['symbol'],
                    'price': coin_data['current_price'],
                    'market_cap': coin_data['market_cap'],
                    'volume_24h': coin_data['total_volume'],
                    'change_24h': coin_data['price_change_percentage_24h'],
                }
            )

        # Retrieve the data from the database
        coins = Coin.objects.all()

        return render(request, 'watchlist.html', {'coins': coins})
    except requests.RequestException as e:
        # Log the exception for debugging purposes
        print(f"Error fetching data from CoinGecko API: {e}")
        # Return a generic error response
        return HttpResponseServerError("Internal Server Error: Unable to fetch data from CoinGecko API.")