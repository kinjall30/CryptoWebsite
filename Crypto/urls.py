from django.urls import path, include, path
from django.conf import settings
from django.conf.urls.static import static
from . import views
# from CryptoCrackers import views
from .views import signup, user_login, index, watchlist, logout_view

app_name = 'CoinCraft'

urlpatterns = [
    path('', views.landing_page, name='index'),
    path('login/', views.user_login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('portfolio/', views.portfolio, name='portfolio'),
    path('crypto_assets/', views.crypto_assets, name='crypto_assets'),
    path('watchlist/', views.watchlist, name='watchlist'),
    path('base/', views.base, name='base'),
    path('profile/', views.user_profile, name='user_profile'),
    path('buy/', views.buy, name='buy'),
    path('sell/', views.sell, name='sell'),
    path('history/', views.transcation_info, name='history'),
    path('logout/', views.logout_view, name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)