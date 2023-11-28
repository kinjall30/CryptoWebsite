# views.py
import requests
from bs4 import BeautifulSoup
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignUpForm, LoginForm
from .models import UserDetails
from .models import UserDetails, Coin
from django.http import HttpResponseServerError
from .models import HistoricalPrice
from datetime import date, timedelta
from django.core.exceptions import ObjectDoesNotExist  # Import the exception
import praw
from .models import CryptoAsset, TrendingCrypto
from .forms import FieldSelectionForm, UserProfileForm, IdentityUploadForm
from .models import UserProfile, Post
from django.shortcuts import get_object_or_404
from django.http import JsonResponse


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            if 'identity' in request.FILES:  # Check if identity file is uploaded
                user.identity_uploaded = True
            user.save()
            return redirect('CryptoCrackers:login')
    else:
        form = SignUpForm()
    return render(request, 'sigup.html', {'form': form})


def base(request):
    return render(request, 'base.html')


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

        print(coins_data[0], "--------------------------------------")

        # Save the data to the database (update or create)
        coins = []
        for coin_data in coins_data:
            try:
                # Check if 'id' is a valid numerical value
                coin = {
                    'name': coin_data['name'],
                    "price": coin_data["current_price"],
                    "symbol": coin_data["symbol"],
                    "market_cap": coin_data["market_cap"],
                    "volume_24h": coin_data["total_volume"],
                    "change_24h": coin_data["price_change_percentage_24h"]
                }
                coins.append(coin)

            except ValueError:
                # Skip entries with invalid 'id'
                continue

            # Coin.objects.update_or_create(
            #     id=coin_id,
            #     defaults={
            #         'name': coin_data['name'],
            #         'symbol': coin_data['symbol'],
            #         'price': coin_data['current_price'],
            #         'market_cap': coin_data['market_cap'],
            #         'volume_24h': coin_data['total_volume'],
            #         'change_24h': coin_data['price_change_percentage_24h'],
            #     }
            # )

        # Retrieve the data from the database
        # coins = Coin.objects.all()

        #         <td>{{ coin.name }}</td>
        # <td>{{ coin.symbol }}</td>
        # <td>${{ coin.price|floatformat:2 }}</td>
        # <td>${{ coin.market_cap|floatformat:2 }}</td>
        # <td>${{ coin.volume_24h|floatformat:2 }}</td>
        # <td>{{ coin.change_24h|floatformat:2 }}%</td>

        print(coins, "--------------rrrrrrrrrrrrrrr")
        return render(request, 'watchlist.html', {'coins': coins, 'tapan': "hello"})
    except requests.RequestException as e:
        # Log the exception for debugging purposes
        print(f"Error fetching data from CoinGecko API: {e}")
        # Return a generic error response
        return HttpResponseServerError("Internal Server Error: Unable to fetch data from CoinGecko API.")


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


def fetch_trending_cryptos_from_api():
    crypto_api_url = 'https://api.coingecko.com/api/v3/coins/markets'
    params = {
        'vs_currency': 'usd',
        'order': 'market_cap_desc',
        'per_page': 5,
        'page': 1,
        'sparkline': False,
    }

    response = requests.get(crypto_api_url, params=params)
    if response.status_code == 200:
        return response.json()
    return []


def landing_page(request):
    trending_cryptos = TrendingCrypto.objects.all()[:10]  # Fetch top 10 cryptocurrencies from local database

    if request.method == 'POST' and 'fetch_latest_data' in request.POST:
        latest_cryptos = fetch_trending_cryptos_from_api()

        # Update or create Trending Crypto instances in the local database
        for crypto in latest_cryptos:
            symbol = crypto['symbol'].lower()
            TrendingCrypto.objects.update_or_create(
                symbol=symbol,
                defaults={
                    'name': crypto['name'],
                    'symbol': symbol,
                    'current_price': crypto['current_price'],
                    # Add more fields as needed
                }
            )

        trending_cryptos = TrendingCrypto.objects.all()[:10]  # Refresh the list from the local database

    community_posts = fetch_community_posts()

    fear_greed_index = fetch_fear_greed_index()
    form = FieldSelectionForm(request.POST or None)

    defaultList = ['name', 'high', 'low', 'price_change_24h', 'price_change_percentage_24h', 'market_cap', 'volume_24h', 'circulating_supply']
    assets = CryptoAsset.objects.values(*defaultList)
   
    if request.method == 'POST' and form.is_valid():
        selected_fields = form.cleaned_data['field_selection']

        # Retrieve only selected fields from the database
        assets = CryptoAsset.objects.values(*selected_fields)
      

        # context = {
        #     'form': form,
        #     'assets': assets,
        # }

    context = {
        'trending_cryptos': trending_cryptos,
        'community_posts': community_posts,
        'fear_greed_index': fear_greed_index,
        'form': form,
        'assets': assets
    }

    return render(request, 'landingpage.html', context)


def crypto_assets(request):
    if request.method == 'POST':
        fetch_new_data = request.POST.get('fetch_new_data')
        if fetch_new_data:
            # API endpoint to fetch cryptocurrency data (replace with actual API endpoint)
            api_url = 'https://api.coingecko.com/api/v3/coins/markets'
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
                        # Check if the cryptocurrency already exists in the database
                        existing_asset = CryptoAsset.objects.filter(name=item['name']).first()

                        if existing_asset:
                            # Update existing data
                            existing_asset.price = item['current_price']
                            existing_asset.high = item['high_24h']
                            existing_asset.low = item['low_24h']
                            existing_asset.price_change_24h = item['price_change_24h']
                            existing_asset.price_change_percentage_24h = item['price_change_percentage_24h']
                            existing_asset.market_cap = item['market_cap']
                            existing_asset.volume_24h = item['total_volume']
                            existing_asset.circulating_supply = item['circulating_supply']
                            # Update other fields as needed

                            existing_asset.save()
                        else:
                            # Create a new cryptocurrency asset
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
                                # Add other fields if necessary
                            )

                            crypto_assets.append(asset)

                # Bulk create new assets if any
                if crypto_assets:
                    CryptoAsset.objects.bulk_create(crypto_assets)

                # Retrieving data from the database
                assets = CryptoAsset.objects.all()
            else:
                assets = CryptoAsset.objects.all()  # Fallback to database if API fails
            # return HttpResponseRedirect('/crypto_assets/')
            return redirect("CryptoCrackers:index")
    # Retrieve data from the database
    assets = CryptoAsset.objects.all()
    context = {
        'crypto_assets': assets,
    }
    return render(request, 'crypto_assets.html', context)

    # return render(request, 'base.html', context)


def user_profile(request):
    user_id = request.session.get('user_id')

    if not user_id:
        return redirect('CryptoCrackers:login')

    user = UserDetails.objects.get(id=user_id)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('CryptoCrackers:user_profile')
    else:
        form = UserProfileForm(instance=user)

    return render(request, 'user_profile.html', {'form': form, 'user': user})


def buy(request):
    if request.method == 'POST':
        selected_currency = request.POST.get('currency')
        quantity = int(request.POST.get('quantity'))

        # Fetch the selected cryptocurrency details
        crypto_assets = CryptoAsset.objects.all()

        # Validate if the selected currency exists
        if selected_currency not in [crypto.name for crypto in crypto_assets]:
            selected_currency = None  # Set selected_currency to None if it's not valid

        # Calculate the total price
        if selected_currency:
            crypto = CryptoAsset.objects.get(name=selected_currency)
            total_price = quantity * crypto.price
        else:
            total_price = None  # Set total_price to None if selected_currency is not valid

        return render(request, 'buy.html', {
            'crypto_assets': crypto_assets,
            'selected_currency': selected_currency,
            'total_price': total_price,
        })

    # If it's a GET request or no valid currency is selected yet
    return render(request, 'buy.html', {
        'crypto_assets': CryptoAsset.objects.all(),
        'selected_currency': None,
        'total_price': None,
    })
def sell(request):
    if request.method == 'POST':
        selected_currency = request.POST.get('currency')
        quantity = int(request.POST.get('quantity'))

        # Fetch the selected cryptocurrency details
        crypto_assets = CryptoAsset.objects.all()

        # Validate if the selected currency exists
        if selected_currency not in [crypto.name for crypto in crypto_assets]:
            selected_currency = None  # Set selected_currency to None if it's not valid

        # Calculate the total price
        if selected_currency:
            crypto = CryptoAsset.objects.get(name=selected_currency)
            total_price = quantity * crypto.price
        else:
            total_price = None  # Set total_price to None if selected_currency is not valid

        return render(request, 'sell.html', {
            'crypto_assets': crypto_assets,
            'selected_currency': selected_currency,
            'total_price': total_price,
        })

    # If it's a GET request or no valid currency is selected yet
    return render(request, 'sell.html', {
        'crypto_assets': CryptoAsset.objects.all(),
        'selected_currency': None,
        'total_price': None,
    })