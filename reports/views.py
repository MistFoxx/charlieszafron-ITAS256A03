from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from django.contrib.auth.models import User
from events.models import Event, Registration

def is_admin(user):
    return user.is_superuser

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
    registrations = Registration.objects.filter(user=request.user)
    events = [registration.event for registration in registrations]
    return render(request, 'registered_event_list.html', {'events': events})

@user_passes_test(is_admin)
def event_registrants(request):
    events = Event.objects.all().prefetch_related('registration_set__user')
    return render(request, 'event_registrants.html', {'events': events})