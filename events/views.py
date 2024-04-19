from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Event, Registration
from django.utils import timezone
from .forms import EventForm

def is_admin(user):
    return user.is_superuser

@login_required
def event_list(request):
    today = timezone.now().date()
    events = Event.objects.filter(end_date__gte=today).prefetch_related('registration_set')
    for event in events:
        # Directly add a registration status attribute to each event
        event.is_registered = event.registration_set.filter(user=request.user).exists()

    return render(request, 'event_list.html', {'events': events})


@user_passes_test(is_admin)
def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save()
            return redirect('event_list')
    else:
        form = EventForm()
    return render(request, 'event_form.html', {'form': form})

@user_passes_test(is_admin)
def event_update(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('event_list')
    else:
        form = EventForm(instance=event)
    return render(request, 'event_form.html', {'form': form})

@user_passes_test(is_admin)
def event_delete(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    event.delete()
    return redirect('event_list')

@login_required
def event_register(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    # Check if the user is already registered to prevent duplicate registrations
    if not Registration.objects.filter(user=request.user, event=event).exists():
        Registration.objects.create(user=request.user, event=event)
        print(f"User {request.user.username} registered for event {event.name}")
    else:
        print(f"User {request.user.username} is already registered for {event.name}")
    return redirect('event_list')


@login_required
def event_unregister(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    Registration.objects.filter(user=request.user, event=event).delete()
    return redirect('event_list')