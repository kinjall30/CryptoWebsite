# views.py
from bs4 import BeautifulSoup
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignUpForm, LoginForm
from .models import UserDetails
import requests
from .models import HistoricalPrice
from datetime import date, timedelta
from django.core.exceptions import ObjectDoesNotExist  # Import the exception
import praw
from .models import CryptoAsset
from .forms import FieldSelectionForm
from .models import UserProfile, Post
from django.shortcuts import get_object_or_404

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
    return render(request, 'landingpage.html')

def portfolio(request):
    return render(request, 'portfolio.html')


def fetch_fear_greed_index():
    # CNN Fear & Greed Index API endpoint
    fear_greed_index_api_url = 'https://money.cnn.com/data/fear-and-greed/'

    # Making a GET request to CNN Fear & Greed Index API
    response = requests.get(fear_greed_index_api_url)

    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        try:
            # Search for specific text indicating Fear & Greed Index value
            index_value = soup.find(text="Fear & Greed Now:").find_next('span').text.strip()
        except AttributeError:
            index_value = None  # Handle when the attribute or element is not found

    else:
        index_value = None  # Handle error scenario when API request fails

    return index_value

def fetch_community_posts():
    # Reddit API credentials (you need to get your own credentials by creating a Reddit app)
    reddit = praw.Reddit(client_id='N3GF_LZQ4KasM5vupgz9Vg',
                         client_secret='sdkxKWOnESPSKCcqqQbU3asw6mERjw',
                         user_agent='This-Egg6458')

    # Fetch posts from the CryptoCurrency subreddit
    subreddit = reddit.subreddit('CryptoCurrency')
    community_posts = []
    for post in subreddit.hot(limit=5):  # Get top 5 hot posts
        community_posts.append({
            'title': post.title,
            'content': post.selftext,
            'author': post.author.name if post.author else 'Unknown Author',
        })
    return community_posts

def landing_page(request):
    # CoinGecko API endpoint for fetching cryptocurrency data
    crypto_api_url = 'https://api.coingecko.com/api/v3/coins/markets'

    # Parameters for the API request (get top 5 cryptocurrencies in USD)
    params = {
        'vs_currency': 'usd',
        'order': 'market_cap_desc',
        'per_page': 5,
        'page': 1,
        'sparkline': False,
    }

    # Making a GET request to CoinGecko API
    response = requests.get(crypto_api_url, params=params)
    print(response.json())
    if response.status_code == 200:
        trending_cryptos = response.json()  # Extracting JSON data if request is successful
        print(trending_cryptos)
    else:
        trending_cryptos = []  # Handling error scenario when API request fails

    # Calculate percentage fluctuation for each cryptocurrency
    for crypto in trending_cryptos:
        symbol = crypto['symbol'].lower()
        try:
            # Get the most recent historical price for the cryptocurrency
            latest_price = HistoricalPrice.objects.filter(cryptocurrency=symbol).latest('date')

            if latest_price:
                previous_price = latest_price.price
                current_price = crypto['current_price']
                crypto['fluctuation_percentage'] = ((current_price - previous_price) / previous_price) * 100
            else:
                crypto['fluctuation_percentage'] = None  # Handle missing previous price
        except ObjectDoesNotExist:  # Handle DoesNotExist exception
            crypto['fluctuation_percentage'] = None  # Handle missing historical price record

    community_posts = fetch_community_posts()

    fear_greed_index = fetch_fear_greed_index()
    form = FieldSelectionForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        selected_fields = form.cleaned_data['field_selection']

        # Retrieve only selected fields from the database
        assets = CryptoAsset.objects.values(*selected_fields)

        context = {
            'form': form,
            'assets': assets,
        }
        return render(request, 'display_selected_fields.html', context)

    context = {
        'trending_cryptos': trending_cryptos,
        'community_posts': community_posts,
        'fear_greed_index': fear_greed_index,
        'form': form
        # Other context data
    }

    return render(request, 'landingpage.html', context)


def crypto_assets(request):
    # API endpoint to fetch cryptocurrency data (replace with actual API endpoint)
    api_url = 'https://api.coingecko.com/api/v3/coins/markets'
    # CryptoAsset.objects.all().delete()
    # Parameters for the API request
    params = {
        'vs_currency': 'usd',
        'order': 'market_cap_desc',
        'per_page': 50,
        'page': 1,
        'sparkline': False,
    }

    # Making a GET request to fetch cryptocurrency data from the API
    response = requests.get(api_url, params=params)

    if response.status_code == 200:
        data = response.json()
        crypto_assets = []

        for item in data:
            # Check if all necessary fields are present in the API response
            if all(key in item for key in ['name', 'current_price', 'high_24h', 'low_24h',
                                           'price_change_24h', 'price_change_percentage_24h',
                                           'market_cap', 'total_volume', 'circulating_supply']):
                asset = CryptoAsset(
                    name=item['name'],
                    price=item['current_price'],
                    high=item['high_24h'],
                    low=item['low_24h'],
                    price_change_24h=item['price_change_24h'],
                    price_change_percentage_24h=item['price_change_percentage_24h'],
                    market_cap=item['market_cap'],
                    volume_24h=item['total_volume'],
                    circulating_supply=item['circulating_supply'],
                    # icon_url=item['image']
                )

                crypto_assets.append(asset)

        # Saving fetched data into the database
        CryptoAsset.objects.bulk_create(crypto_assets)

        # Retrieving data from the database
        assets = CryptoAsset.objects.all()
    else:
        assets = CryptoAsset.objects.all()  # Fallback to database if API fails

    context = {
        'crypto_assets': assets,
    }
    return render(request, 'crypto_assets.html', context)


def user_posts(request, user_id):
    # This will fetch the user id from url
    user = get_object_or_404(UserProfile, user_id=user_id)

    # This will fetch all the post
    posts = Post.objects.filter(author=user)

    return render(request, 'user_posts.html', {
        'user_posts': posts,
        'user_profile': user
    })