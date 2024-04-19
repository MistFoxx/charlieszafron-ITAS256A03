from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.user_list, name='user_list'),
    path('events/', views.event_list, name='event_list'),
    path('events/all/', views.all_event_list, name='all_event_list'),
    path('events/registered/', views.registered_event_list, name='registered_event_list'),
    path('events/registrants/', views.event_registrants, name='event_registrants'),
]
