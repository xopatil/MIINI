from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from .forms import CustomUserCreationForm
import logging

logger = logging.getLogger(__name__)

def index(request):
    print(request.user)
    
    return render(request, 'index.html')

def loginUser(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        username = request.POST.get('username')
        
        logger.debug(f'Attempting login for user: {username}')
        logger.debug(f'Received email: {email}, password: {password}, username: {username}')

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user )
            logger.info(f'User {username} authenticated successfully')
            # Redirect the user to the appropriate page, e.g., "index"
            return redirect("chatbot")
        else:
            logger.warning(f'Failed login attempt for user: {username}')
            messages.error(request, f'Incorrect email or password. Please try again.')

    return render(request, 'registration/login.html')

def logoutUser(request):
    logout(request)
    return redirect('login')

def registerUser(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Set additional attributes here if needed
            user.username = form.cleaned_data.get('username')
            user.save()
            login(request, user,backend='django.contrib.auth.backends.ModelBackend')  # Log in the user after successful registration
            return redirect('login')  # Redirect to the index page after successful registration
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def streamlit(request):
    return render(request,'registration/chatbot.html')