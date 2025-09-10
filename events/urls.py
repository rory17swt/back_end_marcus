from django.urls import path
from .views import EventListCreate, EventDetailView

urlpatterns = [
    path('events/', EventListCreate.as_view()),
    path('events/<int:pk>/', EventDetailView.as_view())
]
