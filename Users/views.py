from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserRegistrationForm
from django.contrib import messages

def home(request):
    return render(request, 'productshop/home.html')

def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome {user.username}!')
            return redirect('product_shop:home')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()

    return render(request, 'users/login.html', {'form': form})

def logout_user(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('users:login_user')

def register_user(request):
    if request.method == 'POST':
        form = CustomUserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful. Please log in to continue.')
            return redirect('users:login_user')  # Redirect to login page after registration
    else:
        form = CustomUserRegistrationForm()
    return render(request, 'users/register.html', {'form': form})
