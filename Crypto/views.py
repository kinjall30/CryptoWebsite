# views.py
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import SignUpForm, LoginForm, UserProfileForm
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


# My added code below
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


def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('CryptoCrackers:login')
