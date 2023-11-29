from django.urls import path
from . import views


urlpatterns = [
    path('', views.payment_view, name='Payments'),
    path('success/', views.payment_success_view, name='Payments_Success'),
]