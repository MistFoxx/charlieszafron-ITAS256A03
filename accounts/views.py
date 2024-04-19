from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import CustomUserCreationForm
from accounts.models import User
from events.models import Event
from datetime import timezone

def is_admin(user):
    return user.is_superuser

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('event_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('landing_page')
        else:
            error_message = 'Invalid username or password.'
            return render(request, 'login.html', {'error_message': error_message})
    else:
        return render(request, 'login.html')
    
@login_required
def landing_page(request):
    return render(request, 'landing_page.html')

@user_passes_test(is_admin)
def user_list(request):
    users = User.objects.all()
    return render(request, 'user_list.html', {'users': users})

def event_list(request):
    events = Event.objects.filter(end_date__gte=timezone.now().date())
    return render(request, 'event_list.html', {'events': events})

@user_passes_test(is_admin)
def all_event_list(request):
    events = Event.objects.all()
    return render(request, 'all_event_list.html', {'events': events})

@login_required
def registered_event_list(request):
    events = request.user.registered_events.all()
    return render(request, 'registered_event_list.html', {'events': events})

@user_passes_test(is_admin)
def event_registrants(request):
    events = Event.objects.all()
    return render(request, 'event_registrants.html', {'events': events})

def logout_view(request):
    logout(request)
    return redirect('login')