from django.urls import path
from . import views

urlpatterns = [
    path('events/', views.event_list, name='event_list'),
    path('events/<int:event_id>/register/', views.event_register, name='event_register'),
    path('events/<int:event_id>/unregister/', views.event_unregister, name='event_unregister'),
    path('create/', views.event_create, name='event_create'),
    path('<int:event_id>/update/', views.event_update, name='event_update'),
    path('<int:event_id>/delete/', views.event_delete, name='event_delete'),
]
