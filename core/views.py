

from .models import *
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib import messages
# Create your views here.



from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    logout(request)
    # Redirect to a success page or home page.
    return redirect('landing-page')  # Replace 'home' with the name of your home URL pattern.

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username and password:  # Check if both username and password are provided
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
            
                return redirect('dashboard')  # Assuming you have a 'success' URL name defined in your urls.py
            else:
               
                messages.error(request, 'Invalid username or password.')
        else:
            # Return an error message if either username or password is missing
            messages.error(request, 'Please provide both username and password.')
    return render(request, 'login.html')  # Assuming you have a login.html template in your templates directory

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import RegistrationForm
from .models import Item, UserProfile

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'signup.html', {'form': form})

def homepage(request):
    user_profile = UserProfile.objects.get(user=request.user)
    preferred_colors = user_profile.preferred_colors.split(',')
    preferred_categories = user_profile.preferred_categories.split(',')

    items = Item.objects.filter(color__in=preferred_colors, category__in=preferred_categories)
    return render(request, 'k/home.html', {'items': items})



def recomendations(request):

    user_profile = UserProfile.objects.get(user=request.user)
    preferred_colors = user_profile.preferred_colors.split(',')
    preferred_categories = user_profile.preferred_categories.split(',')

    items = Item.objects.filter(color__in=preferred_colors, category__in=preferred_categories)
    return render(request, 'k/r.html', {'items': items})

def dashboard(request):
    user_profile = UserProfile.objects.get(user=request.user)
    preferred_colors = user_profile.preferred_colors.split(',')
    preferred_categories = user_profile.preferred_categories.split(',')

    items = Item.objects.filter(color__in=preferred_colors, category__in=preferred_categories)
    product = Item.objects.all()
    context = {
        'product':product,
        'items': items
    }
    return render(request, 'k/home.html', context)



