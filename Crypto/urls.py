from django.urls import path, include, path
from django.conf import settings
from django.conf.urls.static import static
from . import views
# from CryptoCrackers import views
from .views import signup, user_login, index, watchlist

app_name = 'CoinCraft'

urlpatterns = [
    path('', views.landing_page, name='index'),
    path('login/', views.user_login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('portfolio/', views.portfolio, name='portfolio'),
    path('watchlist/', views.watchlist, name='watchlist'),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)