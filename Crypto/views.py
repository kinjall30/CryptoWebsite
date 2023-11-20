# views.py
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignUpForm, LoginForm
from .models import UserDetails


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
